# Create your views here
import json
from utils.common import *
from utils.checkinfo import *
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django import views
from school import models as sc_models
from Django_apps.students import models as stu_models


class StudentInfo(views.View):
    '''
    跳转学生填表页面
    '''

    start_time = []

    def get(self, request, nid, *args, **kwargs):
        step = request.GET.get('step', 'start_page')
        setting_obj = sc_models.TableSettings.objects.filter(id=nid).first()
        result = self.check(setting_obj)
        if result:
            return result
        self.start_time.append(time.time())
        if hasattr(self, step):
            func = getattr(self, step)
            return func(request, setting_obj)

    def post(self, request, nid, *args, **kwargs):
        '''
        提交登陆信息
        :param request:
        :param nid:
        :param args:
        :param kwargs:
        :return:
        '''
        
        self.message = {
            'state': False,
            'msg': '',
            'data': []
        }

        stu_name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        grade = request.POST.get('classes')
        stu_class = request.POST.get('classess')

        filter_condition = {}
        if stu_name:
            filter_condition['full_name'] = stu_name.strip()
        if birthday:
            filter_condition['birthday'] = birthday
        if grade:
            filter_condition['grade'] = grade
        if stu_class:
            filter_condition['stu_class'] = stu_class

        stu_obj = stu_models.StudentInfo.objects.filter(**filter_condition).first()
        setting_obj = sc_models.TableSettings.objects.filter(id=nid).first()
        if not stu_obj:
            self.message['msg'] = '您好，你所填学生信息与学校记录不符，请查证后再填'
            return JsonResponse(self.message)
        else:
            table_info = sc_models.TableInfo.objects.filter(table=setting_obj, student=stu_obj)
            if table_info:
                self.message['msg'] = '该学生已填写完成,无法再次填写'
                return JsonResponse(self.message)
            self.message['state'] = True
            self.message['student_id'] = stu_obj.pk
            return JsonResponse(self.message)

    def check(self, setting_obj):
        '''
        表单校验
        :param setting_obj:
        :return:
        '''
        if not setting_obj:
            return HttpResponse('该表单不存在或已过期')
        if setting_obj.status == 2:
            return HttpResponse('表单暂未发布')
        start_time = setting_obj.stat_time
        end_time = setting_obj.end_time
        current_time = datetime.date.today()
        if current_time < start_time:
            return HttpResponse('填表时间还未开始')
        if end_time:
            if current_time > end_time:
                return HttpResponse('填表已结束')

    def start_page(self, request, setting_obj):
        '''
        登录页
        :param request:
        :param setting_obj:
        :return:
        '''
        school_obj = setting_obj.school_range.first()
        login_fields = setting_obj.login_fields.all()
        return render(request, 'entrance/landing.html',
                      {'setting_obj': setting_obj, 'school_obj': school_obj, 'login_fields': login_fields})

    def stu_info_page(self, request, setting_obj):
        '''
        学生信息页
        :param request:
        :param setting_obj:
        :return:
        '''
        school_obj = setting_obj.school_range.first()
        student_id = request.GET.get('student_id')
        if not student_id:
            self.message['msg'] = '您好，请先填写登陆页面'
            return JsonResponse(self.message)
        student_obj = stu_models.StudentInfo.objects.filter(id=student_id).first()
        stu_field_list = sc_models.SettingToField.objects.order_by('order').filter(setting=setting_obj,
                                                                                   fields__field_type=1).values(
            'fields__fieldName', 'fields__pk', 'is_required')
        if stu_field_list:
            return render(request, 'entrance/student_info.html',
                          {'stu_field_list': stu_field_list, 'pk': setting_obj.pk, 'student_obj': student_obj,
                           'school_obj': school_obj})
        return self.health_page(request, setting_obj)

    def health_page(self, request, setting_obj):
        '''
        健康信息页
        :param request:
        :param setting_obj:
        :return:
        '''
        hel_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=2).values(
            'fields__fieldName', 'fields__pk', 'is_required')
        if hel_field_list:
            return render(request, 'entrance/health_info.html',
                          {'hel_field_list': hel_field_list, 'pk': setting_obj.pk})
        return self.family_page(request, setting_obj)

    def family_page(self, request, setting_obj):
        '''
        家庭信息页
        :param request:
        :param setting_obj:
        :return:
        '''
        fam_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=3).values(
            'fields__fieldName', 'fields__pk', 'is_required')
        if fam_field_list:
            school_district = setting_obj.school_range.values('province', 'city', 'region').first()
            return render(request, 'entrance/family_info.html',
                          {'fam_field_list': fam_field_list, 'pk': setting_obj.pk,
                           'school_district': json.dumps(school_district)})
        return self.parents_page(request, setting_obj)

    def parents_page(self, request, setting_obj):
        '''
        家长信息页
        :param request:
        :param setting_obj:
        :return:
        '''
        par_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=4).values(
            'fields__fieldName', 'fields__pk', 'is_required').order_by('order')

        if par_field_list:
            par_field_json = []
            for item in par_field_list:
                par_field_json.append(item.get('fields__fieldName'))
            return render(request, 'entrance/parent_info.html',
                          {'fam_field_list': par_field_list, 'pk': setting_obj.pk,
                           'par_field_json': json.dumps(par_field_json)})

        return self.question_page(request, setting_obj)

    def question_page(self, request, setting_obj):
        # 自定制问题页面, 如矩阵列表,单选多选
        scale_list = setting_obj.scale.all()
        single_choice_list = setting_obj.choice.filter(choice_type=1)
        multi_choice_list = setting_obj.choice.filter(choice_type=2)

        if scale_list or single_choice_list:
            return render(request, 'entrance/questions.html', {'scale_list': scale_list, 'pk': setting_obj.pk,
                                                               'single_choice_list': single_choice_list,
                                                               'multi_choice_list': multi_choice_list})
        return self.finish_page(request, setting_obj)

    def finish_page(self, request, setting_obj):
        student_id = request.GET.get('student_id')
        parent_id = request.GET.get('parentId')
        end_time = time.time() - self.start_time[0]
        create_dict = {
            'table': setting_obj, 'student_id': student_id, 'finish_time': int(end_time),

        }
        if parent_id and parent_id != 'null':
            parent_obj = StudentParents.objects.filter(id=parent_id).first()
            create_dict['content_object'] = parent_obj

        sc_models.TableInfo.objects.get_or_create(defaults=create_dict, table=setting_obj, student_id=student_id)

        peroration = setting_obj.peroration
        return render(request, 'entrance/End.html', {'peroration': peroration})
