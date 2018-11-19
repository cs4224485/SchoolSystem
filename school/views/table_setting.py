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
        data = request.body
        data = data.decode('utf-8')
        data = json.loads(data).get('data')
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
                models.ScaleLineTitle.objects.create(des=line.get('text'), scale_table=scale_obj)

            # 创建选项的描述
            for option_des in scale_item.get('scaleDes'):
                models.ScaleOptionDes.objects.create(des=option_des.get('text'), scale_table=scale_obj)

        # 添加单选多选表
        for choice_item in data.get('choiceTable'):
            # 创建选择表对象
            obj = models.ChoiceTable.objects.create(title=choice_item.get('title'), setting_table=setting_obj,
                                                    choice_type=choice_item.get('type'))
            # 创建选项的描述
            for op in choice_item.get('optionDes'):
                models.ChoiceOptionsDes.objects.create(des=op.get('contents'), choice_table=obj)

        return JsonResponse({'setting_obj_id': setting_obj.pk})

    return render(request, 'setting/schoolsettiongs.html', {'school_list': school_list})


class TableSetting(object):
    def __init__(self, field_dic, select_field, scope, setting_obj, scale, choice_tb):
        '''
        将表单设置相关的信息封装进一个类
        :return:
        '''
        self.field_dic = field_dic
        self.select_field = select_field
        self.scope = scope
        self.setting_obj = setting_obj
        self.scale = scale
        self.choice_tb = choice_tb


def edit_school_setting(request, nid):
    '''
    编辑设置
    :param request:
    :param nid:
    :return:
    '''
    setting_obj = models.TableSettings.objects.filter(id=nid).first()
    if request.is_ajax():
        try:
            data = request.body
            data = data.decode('utf-8')
            data = json.loads(data).get('data')
            # 更新填表学校
            setting_obj.school_range.set(data['school'])
            # 更新填表范围
            setting_obj.fill_range.set(data['range'])
            # 更新设置信息
            models.TableSettings.objects.filter(pk=nid).update(title=data['title'], stat_time=data['statTime'],
                                                               end_time=data['endTime'])

            # 更新选中的字段
            new_fields_ids = [int(field_id) for field_id in data.get('choiceFieldId')]
            old_fields = models.SettingToField.objects.filter(setting=setting_obj).all().distinct().order_by('order')
            old_fields_ids = [item.fields.pk for item in old_fields]
            temp = []
            for field in new_fields_ids:
                index = new_fields_ids.index(field)

                if field not in old_fields_ids:
                    obj = models.SettingToField.objects.create(setting=setting_obj, fields_id=int(field), order=index)
                    temp.append(obj)
                    temp.append(obj.pk)
                elif index != old_fields_ids.index(field):
                    models.SettingToField.objects.filter(setting=setting_obj, fields_id=int(field)).update(order=index)
            new_fields_ids.extend(temp)
            del_fields = list(set(old_fields_ids).difference(new_fields_ids))
            for item in del_fields:
                models.SettingToField.objects.filter(fields_id=item).delete()

            # 更新量表
            scale_info = data.get('scaleTable')
            update_scale_table(scale_info, setting_obj)

            # 更新或新增选项表
            choice_info = data.get('choiceTable')
            update_choice_table(choice_info, setting_obj)
            return JsonResponse({'setting_obj_id': setting_obj.pk, 'state': True})
        except Exception as e:
            return JsonResponse({'state': False})

    # 查询出已设置的字段信息
    field_dict = {}
    field_type = ('stu_field_list', 'hel_field_list', 'fam_filed_list', 'par_field_list')
    for i in range(1, 5):
        field_dict[field_type[i - 1]] = models.SettingToField.objects.filter(setting=setting_obj,
                                                                             fields__field_type=i).values(
            'fields__fieldName', 'fields__pk').order_by('order')
    selected_fields = json.dumps(list(setting_obj.settingtofield_set.values_list('fields__fieldName', )))
    # 填表范围信息
    scope_of_filling = models.ScopeOfFilling.objects.all()
    # 矩阵表信息
    scale_list = setting_obj.scale.all()
    # 单选多选表信息
    choice_tb_list = setting_obj.choice.all()
    tb_info = TableSetting(field_dict, selected_fields, scope_of_filling, setting_obj, scale_list, choice_tb_list)
    return render(request, 'setting/edit_setting.html', {'tb_info': tb_info})


def update_choice_table(choice_info,setting_obj ):
    '''
    根据提交的数据更新选项表
    :param choice_info:
    :param setting_obj:
    :return:
    '''

    choice_l = []
    for table_item in choice_info:
        table_id = table_item.get('id')
        table_title = table_item.get('title')
        options = table_item.get('optionDes')
        choice_type = table_item.get('type')
        if not table_id:
            obj = models.ChoiceTable.objects.create(title=table_title, choice_type=choice_type,
                                                    setting_table=setting_obj)
            for op_item in options:
                models.ChoiceOptionsDes.objects.create(des=op_item.get('contents'), choice_table=obj)
            choice_l.append(obj.pk)
        else:
            choice_l.append(int(table_id))
            old_option = models.ChoiceOptionsDes.objects.filter(choice_table_id=int(table_id)).only('id')
            old_option_ids = [item.pk for item in old_option]
            # 更新或添加选择表中的选项
            new_option_ids = []
            if options:
                for op in options:
                    option_id = op.get('id')
                    content = op.get('contents')
                    if not option_id:
                        op_obj = models.ChoiceOptionsDes.objects.create(des=content, choice_table_id=int(table_id))
                        new_option_ids.append(op_obj.pk)
                    else:
                        new_option_ids.append(int(option_id))
                        models.ChoiceOptionsDes.objects.filter(id=int(option_id)).update(des=content)
            del_option_ids = list(set(old_option_ids).difference(new_option_ids))
            for item_id in del_option_ids:
                models.ChoiceOptionsDes.objects.filter(id=item_id).delete()
    old_table = models.ChoiceTable.objects.filter(setting_table=setting_obj).only('id')
    old_table_ids = [item.id for item in old_table]
    del_table_ids = list(set(old_table_ids).difference(choice_l))
    for del_id in del_table_ids:
        models.ChoiceTable.objects.filter(id=del_id).delete()


def update_scale_table(scale_info, setting_obj):
    '''
    根据提交的数据创建或更新矩阵量表信息
    :param scale_info: 量表信息
    :param setting_obj: 表单对象
    :return:
    '''
    scale_l = []
    for scale in scale_info:
        scale_id = scale.get('id')
        scale_title = scale.get('scaleTitle')
        line_title = scale.get('lineTitle')
        scale_des = scale.get('scaleDes')
        if scale_id:
            scale_l.append(int(scale_id))
        if not scale_id:
            # 如果ID不存在代表新创建的表
            scale_obj = models.ScaleSetting.objects.create(title=scale_title, setting_table=setting_obj)
            for line in line_title:
                models.ScaleLineTitle.objects.create(des=line.get('text'), scale_table=scale_obj)
            for option in scale_des:
                models.ScaleOptionDes.objects.create(des=option.get('text'), scale_table=scale_obj)

            scale_l.append(scale_obj.pk)
        else:
            models.ScaleSetting.objects.filter(id=int(scale_id)).update(title=scale_title)
            old_line_title = models.ScaleLineTitle.objects.filter(scale_table_id=int(scale_id)).only('id')
            old_line_ids = [line.id for line in old_line_title]
            old_option_des = models.ScaleOptionDes.objects.filter(scale_table_id=int(scale_id)).only('id')
            old_option_ids = [op.id for op in old_option_des]

            new_line_ids = []
            new_option_ids = []
            # 创建或更新行标题
            if line_title:
                for line in line_title:
                    line_id = line.get('id')
                    content = line.get('text')
                    if not line_id:
                        line_obj = models.ScaleLineTitle.objects.create(des=content, scale_table_id=scale_id)
                        new_line_ids.append(line_obj.pk)
                    else:
                        new_line_ids.append(int(line_id))
                        models.ScaleLineTitle.objects.filter(id=int(line_id)).update(des=content)
            # 删除旧的行标题
            del_line_id = list(set(old_line_ids).difference(new_line_ids))
            for item_id in del_line_id:
                models.ScaleLineTitle.objects.filter(id=item_id).delete()

            # 创建或更新选项描述
            if scale_des:
                for option in scale_des:
                    option_id = option.get('id')
                    content = option.get('text')
                    if not option_id:
                        option_obj = models.ScaleOptionDes.objects.create(des=content, scale_table_id=int(scale_id))
                        new_option_ids.append(option_obj.pk)
                    else:
                        new_option_ids.append(int(option_id))
                        models.ScaleOptionDes.objects.filter(id=int(option_id)).update(des=content)
            del_option_id = list(set(old_option_ids).difference(new_option_ids))
            for item_id in del_option_id:
                models.ScaleOptionDes.objects.filter(id=item_id).delete()

    scale_table = models.ScaleSetting.objects.filter(setting_table=setting_obj).only('id')
    old_scale_ids = [item.id for item in scale_table]
    del_scale_ids = list(set(old_scale_ids).difference(scale_l))
    for item_id in del_scale_ids:
        models.ScaleSetting.objects.filter(id=item_id).delete()


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
