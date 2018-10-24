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
        setting_obj = models.SchoolSettings.objects.create(title=data['title'], stat_time=data['statTime'],
                                                           end_time=data['endTime'])

        # 生成的二维码文件名
        qrfile_name = generate_qrcode(setting_obj.pk)
        models.SchoolSettings.objects.filter(id=setting_obj.pk).update(Qrcode=qrfile_name)

        # 填表学校
        setting_obj.school_range.add(*data['school'])
        # 填表范围
        setting_obj.fill_range.add(*data['range'])

        temp = []
        index = 1
        for field in data['choiceFieldId']:
            obj = models.SettingToField(setting=setting_obj, fields_id=int(field), order=index)
            temp.append(obj)
            index += 1
        models.SettingToField.objects.bulk_create(temp)

        return JsonResponse({'setting_obj_id': setting_obj.pk})

    return render(request, 'setting/schoolsettiongs.html', {'school_list': school_list})


def edit_school_setting(request, nid):
    '''
    编辑设置
    :param request:
    :param nid:
    :return:
    '''
    setting_obj = models.SchoolSettings.objects.filter(id=nid).first()
    if request.is_ajax():
        data = json.loads(request.POST.get('data'))
        # 更新填表学校
        setting_obj.school_range.set(data['school'])
        # 更新填表范围
        setting_obj.fill_range.set(data['range'])
        # 更新设置信息
        models.SchoolSettings.objects.filter(pk=nid).update(title=data['title'], stat_time=data['statTime'],
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

        return JsonResponse({'setting_obj_id': setting_obj.pk})

    stu_field_list = models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=1).values(
        'fields__fieldName', 'fields__pk')
    hel_field_list = models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=2).values(
        'fields__fieldName', 'fields__pk')
    fam_filed_list = models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=3).values(
        'fields__fieldName', 'fields__pk')
    par_field_list = models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=4).values(
        'fields__fieldName', 'fields__pk')

    selected_fields = json.dumps(list(setting_obj.settingtofield_set.values_list('fields__fieldName', )))
    scope_of_filling = models.ScopeOfFilling.objects.all()
    return render(request, 'setting/edit_setting.html',
                  {"stu_field_list": stu_field_list, "hel_field_list": hel_field_list,
                   "fam_filed_list": fam_filed_list, "par_field_list": par_field_list,
                    'setting_obj': setting_obj, "selected_fields": selected_fields, 'scope': scope_of_filling})


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

    return HttpResponse('ok')


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
    setting_obj = models.SchoolSettings.objects.filter(id=nid).first()
    qrfile = os.path.join('/media/school/Qrcode/', setting_obj.Qrcode)
    url = '%s/student/student_info/%s/' % (settings.DOMAIN_NAME, nid)
    return render(request, 'setting/release.html', {'qrfile': qrfile, "url":url})



