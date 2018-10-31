from django.shortcuts import render, HttpResponse
from school import models
from django.conf import settings
from school.utils.common_utils import *
from django.http import JsonResponse
import json
import os


# Create your views here.

def school_setting(request):
    '''
    学校设置页面
    :param request:
    :return:
    '''
    school_list = models.SchoolInfo.objects.all()
    if request.is_ajax():
        data = json.loads(request.POST.get('data'))

        # 将学校选中需要填写的字段保存至数据库
        setting_obj = models.TableSettings.objects.create(title=data['title'], stat_time=data['statTime'],
                                                           end_time=data['endTime'])
        # 生成的二维码文件名
        qrfile_name = generate_qrcode(setting_obj.pk)
        models.TableSettings.objects.filter(id=setting_obj.pk).update(Qrcode=qrfile_name)

        # 填表学校
        setting_obj.school_range.add(*data['school'])
        # 填表范围
        setting_obj.fill_range.add(*data['range'])

        # 添加表单与字段的对应
        temp = []
        index = 1
        for field in data['choiceFieldId']:
            obj = models.SettingToField(setting=setting_obj, fields_id=int(field), order=index)
            temp.append(obj)
            index += 1
        models.SettingToField.objects.bulk_create(temp)

        # 添加矩阵量表
        for scale_item in data.get('scaleTable'):
            # 创建量表对象
            scale_obj = models.ScaleSetting.objects.create(title=scale_item.get('scaleTitle'),
                                                           setting_table=setting_obj)
            # 创建行标题
            for line in scale_item.get('lineTitle'):
                models.ScaleLineTitle.objects.create(des=line, scale_table=scale_obj)

            # 创建选项的描述
            for option_des in scale_item.get('scaleDes'):
                models.ScaleOptionDes.objects.create(des=option_des, scale_table=scale_obj)
        return JsonResponse({'setting_obj_id': setting_obj.pk})

    return render(request, 'setting/schoolsettiongs.html', {'school_list': school_list})


class TableSetting(object):
    def __init__(self, field_dic, select_field, scope, setting_obj, scale):
        '''
        将表单设置相关的信息封装进一个类
        :return:
        '''
        self.field_dic = field_dic
        self.select_field = select_field
        self.scope = scope
        self.setting_obj = setting_obj
        self.scale = scale


def edit_school_setting(request, nid):
    '''
    编辑设置
    :param request:
    :param nid:
    :return:
    '''
    setting_obj = models.TableSettings.objects.filter(id=nid).first()
    if request.is_ajax():
        data = json.loads(request.POST.get('data'))
        # 更新填表学校
        setting_obj.school_range.set(data['school'])
        # 更新填表范围
        setting_obj.fill_range.set(data['range'])
        # 更新设置信息
        models.TableSettings.objects.filter(pk=nid).update(title=data['title'], stat_time=data['statTime'],
                                                            end_time=data['endTime'])
        # 删除之前的配置再重建新的字段
        models.SettingToField.objects.filter(setting=setting_obj).delete()
        temp = []
        index = 1
        for field in data['choiceFieldId']:
            obj = models.SettingToField(setting=setting_obj, fields_id=int(field), order=index)
            temp.append(obj)
            index += 1
        models.SettingToField.objects.bulk_create(temp)
        # 删除之前的量表信息
        models.ScaleSetting.objects.filter(setting_table=setting_obj).delete()
        # 添加矩阵量表
        for scale_item in data.get('scaleTable'):
            # 创建量表对象
            scale_obj = models.ScaleSetting.objects.create(title=scale_item.get('scaleTitle'),
                                                           setting_table=setting_obj)
            # 创建行标题
            for line in scale_item.get('lineTitle'):
                models.ScaleLineTitle.objects.create(des=line, scale_table=scale_obj)

            # 创建选项的描述
            for option_des in scale_item.get('scaleDes'):
                models.ScaleOptionDes.objects.create(des=option_des, scale_table=scale_obj)

        return JsonResponse({'setting_obj_id': setting_obj.pk})

    # 查询出已设置的字段信息
    field_dict = {}
    field_type = ('stu_field_list', 'hel_field_list', 'fam_filed_list', 'par_field_list')
    for i in range(1, 5):
        field_dict[field_type[i - 1]] = models.SettingToField.objects.filter(setting=setting_obj,
                                                                             fields__field_type=i).values(
                                                                            'fields__fieldName', 'fields__pk')
    selected_fields = json.dumps(list(setting_obj.settingtofield_set.values_list('fields__fieldName', )))
    # 填表范围信息
    scope_of_filling = models.ScopeOfFilling.objects.all()
    # 矩阵表信息
    scale_list = setting_obj.scale.all()
    tb_info = TableSetting(field_dict, selected_fields, scope_of_filling, setting_obj,  scale_list)
    return render(request, 'setting/edit_setting.html', {'tb_info': tb_info})


def filterSchool(request):
    '''
    根据选择省市区过滤出学校
    :param request:
    :param type:
    :return:
    '''
    if request.method == "GET":
        data = request.GET
        layer = data.get('layer')
        extra = {}
        if layer:
            extra['school_layer'] = layer

        school_list = list(models.SchoolInfo.objects.filter(province=data.get('province'),
                                                            city=data.get('city'), region=data.get('region'),
                                                            **extra).values('school_name', 'pk', 'campus_district'))
        return JsonResponse({'school_list': school_list})


def preview(request):
    '''
    预览页面
    :param request:
    :return:
    '''
    data = json.loads(request.GET.get('data'))
    # stu_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=1)
    # hel_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=2)
    # fam_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=3)
    # par_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=4)
    return render(request, 'setting/perview.html', {'data': data})


def release(request, nid):
    '''
    发布页面
    :param request:
    :param nid:
    :return:
    '''
    setting_obj = models.TableSettings.objects.filter(id=nid).first()
    qrfile = os.path.join('/media/school/Qrcode/', setting_obj.Qrcode)
    url = '%s/student/student_info/%s/' % (settings.DOMAIN_NAME, nid)
    return render(request, 'setting/release.html', {'qrfile': qrfile, "url": url})
