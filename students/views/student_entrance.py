# Create your views here
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django import views
from school import models as sc_models
from students import models as stu_models
import json


class StudentInfo(views.View):
    '''
    跳转学生填表页面
    '''

    def get(self, request, nid, *args, **kwargs):

        step = request.GET.get('step', 'start')
        setting_obj = sc_models.SchoolSettings.objects.filter(id=nid).first()
        if step == 'start':
            school_obj = setting_obj.school_range.first()
            return render(request, 'entrance/landing.html', {'setting_obj': setting_obj, 'school_obj': school_obj})
        if step == '1':
            student_id = request.GET.get('student_id')
            student_obj = stu_models.StudentInfo.objects.filter(id=student_id).first()
            stu_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=1).values(
                'fields__fieldName', 'fields__pk')
            return render(request, 'entrance/student_info.html',
                          {'stu_field_list': stu_field_list, 'pk': setting_obj.pk, 'student_obj': student_obj})
        elif step == '2':
            hel_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=2).values(
                'fields__fieldName', 'fields__pk')
            return render(request, 'entrance/health_info.html',
                          {'hel_field_list': hel_field_list, 'pk': setting_obj.pk})
        elif step == '3':
            fam_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=3).values(
                'fields__fieldName', 'fields__pk')
            return render(request, 'entrance/family_info.html',
                          {'fam_field_list': fam_field_list, 'pk': setting_obj.pk})
        elif step == '4':
            par_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=4).values(
                'fields__fieldName', 'fields__pk')
            par_field_json = []
            for item in par_field_list:
                par_field_json.append(item.get('fields__fieldName'))

            return render(request, 'entrance/parent_info.html',
                          {'fam_field_list': par_field_list, 'pk': setting_obj.pk, 'par_field_json': json.dumps(par_field_json)})

    def post(self, request, nid, *args, **kwargs):
        message = {
            'state': False,
            'msg': '',
            'data': []
        }
        stu_name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        grade = request.POST.get('classes')
        stu_class = request.POST.get('classess')
        stu_obj = stu_models.StudentInfo.objects.filter(full_name=stu_name, birthday=birthday, grade=grade, stu_class=stu_class).first()

        if not stu_obj:
            message['msg'] = '您好，你所填学生信息与学校记录不符，请查证后再填'
            return JsonResponse(message)
        else:
            message['state'] = True
            message['student_id'] = stu_obj.pk
            return JsonResponse(message)