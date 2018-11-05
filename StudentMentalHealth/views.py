from django.shortcuts import render, redirect
from django import views
from teacher import models as th_models
from students import models as stu_models
from school import models as sch_models
from django.http import JsonResponse
from utils.common import get_en_name
from django.utils.decorators import method_decorator
import datetime
import json

# Create your views here.


def login_required(func):
    '''
    要求登陆的装饰器
    :return:
    '''

    def inner(request, *args, **kwargs):
        teacher_id = request.session.get('teacher_id')
        if not teacher_id:
            return redirect('/mental/login/')
        return func(request, *args, **kwargs)
    return inner


class LoinView(views.View):
    '''
    学生心理健康教师登陆
    '''

    def get(self, request, *args, **kwargs):
        return render(request, 'landing.html')

    def post(self, request, *args, **kwargs):
        message = {
            'state': False,
            'data': '',
            'msg': ''
        }
        teacher_name = request.POST.get('name')
        if len(teacher_name) <= 1:
            message['msg'] = '姓名输入有误'
            return JsonResponse(message)
        phone = request.POST.get('phoneNumber')
        teacher_obj = th_models.TeacherInfo.objects.filter(last_name=teacher_name[0], first_name=teacher_name[1::],
                                                           telephone__endswith=phone).first()
        if teacher_obj:
            message['state'] = True
            message['msg'] = '登陆成功'
            request.session['teacher_id'] = teacher_obj.pk
        else:
            message['msg'] = '未匹配到,请核对信息'
        return JsonResponse(message)


class TeacherIndexView(views.View):
    '''
    教师首页
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_id = request.session.get('teacher_id')
        teacher_obj = th_models.TeacherInfo.objects.filter(id=teacher_id).first()
        return render(request, 'teacher_index.html', {'teacher_obj': teacher_obj})


class RecordStudentListView(views.View):
    '''
    记录个别教育学生列表
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_id = request.session.get('teacher_id')
        teacher_info = th_models.TeacherInfo.objects.filter(id=teacher_id).values('school', 'teachers__stu_class__name',
                                                                                  'teachers__stu_class__grade').first()
        grade = teacher_info.get('teachers__stu_class__grade')
        stu_class = sch_models.StuClass.objects.filter(grade=grade, name=teacher_info.get('teachers__stu_class__name'),
                                                       school=teacher_info.get('school')).first()
        student_list = stu_models.StudentInfo.objects.filter(stu_class=stu_class)
        return render(request, 'record_student_list.html', {'class': stu_class, 'student_List': student_list})


class RecordsOfStudents(views.View):
    '''
    学生教育档案
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        student_obj = stu_models.StudentInfo.objects.filter(id=student_id).first()
        teacher_info = th_models.TeacherInfo.objects.filter(id=request.session.get('teacher_id')).values('last_name',
                                                                                                         'school',
                                                                                                         'first_name',
                                                                                                         'identity__title').first()
        en_name = get_en_name(student_obj.full_name)
        current_time = datetime.date.today()
        setting_obj = sch_models.TableSettings.objects.filter(school_range=teacher_info.get('school'), fill_range=1).first()
        scale = setting_obj.scale.first()
        return render(request, 'archivesCont.html',
                      {'student': student_obj, 'teacher_info': teacher_info, 'en_name': en_name,
                       'current_time': current_time, 'scale_item': scale})

    def post(self, request, *args, **kwargs):
        message = {
            'state': False,
            'data': '',
            'msg': ''
        }
        data = json.loads(request.POST.get('info'))
        for scale_id, values in data.get('scaleInfo').items():
            scale_obj = stu_models.ScaleQuestion.objects.create(student_id=data.get('studentId'), scale_id=scale_id)
            for item in values:
                item['scale_stu'] = scale_obj
                stu_models.ScaleValue.objects.create(**item)
        else:
            message['state'] = True
        return JsonResponse(message)


class Appointment(views.View):
    '''
    预约心理老师
    '''
    pass
