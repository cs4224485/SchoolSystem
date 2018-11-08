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

        # 通过姓名和电话号码登陆
        teacher_name = request.POST.get('name')
        if len(teacher_name) <= 1:
            message['msg'] = '姓名输入有误'
            return JsonResponse(message)
        phone = request.POST.get('phoneNumber')
        teacher_obj = th_models.TeacherInfo.objects.filter(last_name=teacher_name[0], first_name=teacher_name[1::],
                                                           telephone__endswith=phone).values('last_name', 'first_name',
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
                'id': teacher_obj.get('id')
            }
            message['state'] = True
            message['msg'] = '登陆成功'
            request.session['teacher_id'] = teacher_obj.get('id')
            request.session['teacher_info'] = teacher_info
        else:
            message['msg'] = '未匹配到,请核对信息'
        return JsonResponse(message)


class TeacherIndexView(views.View):
    '''
    教师首页
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_info = request.session.get('teacher_info')
        stu_class = sch_models.StuClass.objects.filter(id=teacher_info.get('stu_class')).first()
        return render(request, 'teacher_index.html', {'stu_class': stu_class})


class RecordStudentListView(views.View):
    '''
    记录个别教育学生列表
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        teacher_info = request.session.get('teacher_info')
        # 过滤出教师当前管理班级的学生
        grade = teacher_info.get('grade')
        stu_class = sch_models.StuClass.objects.filter(grade=grade, id=teacher_info.get('stu_class'),
                                                       school=teacher_info.get('school')).first()
        student_list = stu_models.StudentInfo.objects.filter(stu_class=stu_class)
        return render(request, 'record_student_list.html', {'class': stu_class, 'student_List': student_list})


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

    message = {
        'state': False,
        'data': '',
        'msg': ''
    }

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
                self.message['msg'] = '创建成功'
                self.message['state'] = True
        except Exception as e:
            print(e)
            self.message['msg'] = '创建失败'
        return JsonResponse(self.message)


class RecordsOfStudents(views.View):
    '''
    查看学生的历史教育档案
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        record_id = kwargs.get('record_id')
        teacher_id = request.session.get('teacher_info').get('id')
        record_obj = mental_models.IndividualStudentRecord.objects.filter(id=record_id, teacher_id=teacher_id).first()
        if record_obj:
            student_obj = record_obj.student
            # 量表信息
            scale = stu_models.ScaleValue.objects.filter(scale_stu=record_obj.scale_table)
            current_time = datetime.date.today()
            # 校历
            school_week = current_week(datetime.datetime.now())

            return render(request, 'show_record.html',
                          {'student': student_obj, 'current_time': current_time, 'scale_item': scale,
                           'school_week': school_week})
        else:
            return HttpResponse('该记录不存在')


class AppointmentTeacher(views.View):
    '''
    预约心理老师
    '''

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        return render(request, 'appointment.html')
