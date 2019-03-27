import datetime
import json
from django.shortcuts import render, redirect
from django import views
from django.shortcuts import HttpResponse
from teacher import models as th_models
from students import models as stu_models
from school import models as sch_models
from StudentMentalHealth import models as mental_models
from django.http import JsonResponse
from utils.common import current_week
from django.utils.decorators import method_decorator
from utils.base_response import BaseResponse


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
        message = BaseResponse()

        # 通过姓名和电话号码登陆
        teacher_name = request.POST.get('name')
        if len(teacher_name) <= 1:
            message.msg = '姓名输入有误'
            return JsonResponse(message)
        phone = request.POST.get('phoneNumber')
        teacher_query = th_models.TeacherInfo.objects.filter(last_name=teacher_name[0], first_name=teacher_name[1::],
                                                             telephone__endswith=phone)
        teacher_obj = teacher_query.values('last_name', 'first_name',
                                           'teachers__stu_class__grade',
                                           'teachers__stu_class',
                                           'school', 'id',
                                           'identity__title').first()

        if teacher_obj:
            # 将老师的信息存放到session中
            teacher_info = {
                'name': teacher_obj.get('last_name') + teacher_obj.get('first_name'),
                'school': teacher_obj.get('school'),
                'grade': teacher_obj.get('teachers__stu_class__grade'),
                'stu_class': teacher_obj.get('teachers__stu_class'),
                'identity': teacher_obj.get('identity__title'),
                'id': teacher_obj.get('id'),
                'is_psychology_teacher': teacher_query.first().course.all().filter(course_des='心理').exists()

            }
            message.state = True
            message.msg = '登陆成功'
            request.session['teacher_id'] = teacher_obj.get('id')
            request.session['teacher_info'] = teacher_info
        else:
            message.msg = '未匹配到,请核对信息'
        return JsonResponse(message.get_dict)


class TeacherIndexView(views.View):
    '''
    教师首页
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_info = request.session.get('teacher_info')
        stu_class = sch_models.StuClass.objects.filter(id=teacher_info.get('stu_class')).first()
        school_id = teacher_info.get('school')
        return render(request, 'teacher_index.html', {'stu_class': stu_class, 'school_id': school_id})


class RecordStudentListView(views.View):
    '''
    个别教育学生列表
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_info = request.session.get('teacher_info')
        teacher_id = teacher_info.get('id')
        school_id = teacher_info.get('school')

        return render(request, 'record_student_list.html', {'teacher_id': teacher_id, 'school_id': school_id})


class RecordList(views.View):
    '''
    每个学生的记录档案列表页
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):

        student_id = kwargs.get('student_id')
        teacher_info = request.session.get('teacher_info')
        student_obj = stu_models.StudentInfo.objects.filter(id=student_id, school=teacher_info.get('school'),
                                                            stu_class=teacher_info.get('stu_class')).first()

        is_psychology_teacher = request.session['teacher_info'].get('is_psychology_teacher')
        if is_psychology_teacher:
            student_obj = stu_models.StudentInfo.objects.filter(id=student_id,
                                                                school=teacher_info.get('school')).first()

        if student_obj:
            record_list = mental_models.IndividualStudentRecord.objects.filter(student_id=student_id)
            # 如果本周已经填写那么无法继续再填
            is_filled = False
            school_week = current_week(datetime.datetime.now())
            if record_list.first():
                record_week = current_week(datetime.datetime.strptime(str(record_list.first().record_time), '%Y-%m-%d'))
                # 如果填写记录的日期与当前校历是同一周，那么表示这周已经填写过了
                if school_week == record_week:
                    is_filled = True
            current_time = datetime.date.today()
            return render(request, 'psychologyList.html',
                          {'student': student_obj, 'record_list': record_list,
                           'current_time': current_time, 'school_week': school_week, 'is_filled': is_filled})

        return HttpResponse('该学生不存在')


class AddRecord(views.View):
    '''
    添加一条学生档案记录
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        student_id = kwargs.get('student_id')
        teacher_info = request.session.get('teacher_info')
        student_obj = stu_models.StudentInfo.objects.filter(id=student_id, school=teacher_info.get('school'),
                                                            stu_class=teacher_info.get('stu_class')).first()
        if student_obj:
            # 获取表单设置信息
            setting_obj = sch_models.TableSettings.objects.filter(school_range=teacher_info.get('school'),
                                                                  fill_range=1).first()

            scale = setting_obj.scale.first()
            return render(request, 'add_record.html', {'student': student_obj, 'scale': scale})
        return HttpResponse('该学生不存在')

    def post(self, request, *args, **kwargs):
        message = BaseResponse()
        try:
            data = json.loads(request.POST.get('info'))
            teacher_id = request.session.get('teacher_info').get('id')
            for scale_id, values in data.get('scaleInfo').items():
                # 创建量表与学生的对应关系
                scale_obj = stu_models.ScaleQuestion.objects.create(student_id=data.get('studentId'), scale_id=scale_id)
                # 创建一条档案记录
                mental_models.IndividualStudentRecord.objects.create(student_id=data.get('studentId'),
                                                                     scale_table=scale_obj, teacher_id=teacher_id)
                for item in values:
                    # 将填写的值与量表相对应
                    item['scale_stu'] = scale_obj
                    stu_models.ScaleValue.objects.create(**item)
            else:
                message.msg = '创建成功'
                message.state = True
        except Exception as e:
            message.msg = '创建失败'
        return JsonResponse(message.get_dict)


class RecordsOfStudents(views.View):
    '''
    查看学生的历史教育档案
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        teacher_info = request.session.get('teacher_info')
        record_obj = mental_models.IndividualStudentRecord.objects.filter(id=record_id).first()
        if teacher_info.get('identity') == '心理老师':
            record_obj = mental_models.IndividualStudentRecord.objects.filter(id=record_id).first()

        if record_obj:
            student_obj = record_obj.student
            # 量表信息
            scale = stu_models.ScaleValue.objects.filter(scale_stu=record_obj.scale_table)
            return render(request, 'show_record.html',
                          {'student': student_obj, 'scale_item': scale, 'record': record_obj})
        else:
            return HttpResponse('该记录不存在')


class AppointmentTeacher(views.View):
    '''
    预约心理老师
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_info = request.session.get('teacher_info')
        class_id = teacher_info.get('stu_class')
        school_id = teacher_info.get('school')
        stu_class = sch_models.StuClass.objects.filter(id=class_id).first()
        current_day = datetime.date.today()
        student_queryset = stu_models.StudentInfo.objects.filter(stu_class=stu_class, school_id=school_id).only('id')
        student_ids = [obj.id for obj in student_queryset]
        appointment_queryset = mental_models.AppointmentManage.objects.filter(
            date__gte=current_day,
            student_id__in=student_ids)
        return render(request, 'about.html', {'class_id': class_id, 'stu_class': stu_class, 'school_id': school_id,
                                              'appointment_info': appointment_queryset})

    def post(self, request, *args, **kwargs):
        message = BaseResponse()
        teacher_id = request.POST.get('teacher_id')
        date = request.POST.get('date')
        time_id = request.POST.get('time_id')
        student_id = request.POST.get('student_id')

        if datetime.datetime.strptime(date, '%Y-%m-%d') < (datetime.datetime.now() - datetime.timedelta(days=1)):
            message.msg = '预约时间有误'
            return JsonResponse(message.get_dict)

        try:
            # 预约创建前先加锁
            from django.db import transaction
            with transaction.atomic():
                appointment_obj = mental_models.AppointmentManage.objects.filter(teacher_id=teacher_id, date=date,
                                                                                 time_id=time_id).select_for_update()
                if appointment_obj:
                    message.msg = '该时段已被预约'
                    return JsonResponse(message.get_dict)

                mental_models.AppointmentManage.objects.create(teacher_id=teacher_id, date=date,
                                                               time_id=time_id, student_id=student_id)
                message.state = True
                message.msg = '预约成功'
        except Exception as e:
            print(e)
            message.msg = '预约失败'
        return JsonResponse(message.get_dict)

    def delete(self, request, *args, **kwargs):
        '''
        根据ID 删除一条预约
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        message = BaseResponse()
        try:
            data = json.loads(request.body.decode('utf-8'))
            appointment_id = data.get('appointmentId')
            mental_models.AppointmentManage.objects.filter(id=appointment_id).delete()
            message.state = True
            message.msg = '删除成功'
        except Exception as e:
            message.msg = '删除失败'
        return JsonResponse(message.get_dict)


class AppointmentManage(views.View):
    '''
    预约管理
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_id = request.session.get('teacher_info').get('id')
        school_id = request.session.get('teacher_info').get('school')
        current_day = datetime.date.today()
        appointment_queryset = mental_models.AppointmentManage.objects.filter(teacher_id=teacher_id,
                                                                              date__gte=current_day)
        return render(request, 'aboutList.html', {'appointment_info': appointment_queryset, 'school_id': school_id})

    def post(self, request, *args, **kwargs):

        '''
        心理老师可修改预约时间
        :return:
        '''
        message = BaseResponse()
        try:
            date = request.POST.get('date')
            appointment_id = request.POST.get('appointmentId')
            mental_models.AppointmentManage.objects.filter(id=appointment_id).update(date=date)
            message.state = True
            message.msg = '修改成功'
        except Exception as e:
            print(e)
            message.msg = '修改失败'
        return JsonResponse(message.get_dict)
