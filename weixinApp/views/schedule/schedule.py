import datetime
from rest_framework.views import APIView, Response
from django.conf import settings
from django.db.models import Q
from utils.base_response import BaseResponse
from weixinApp import models
from weixinApp.service.decorator import *
from weixinApp.service.schedule_service import CourseTableService
from django.utils.decorators import method_decorator
from weixinApp.auth.auth import WeiXinAuth
from students import models as stumodels
from teacher import models as teamodels
from school import models as scmodels
from utils.common import current_week, date_to_datetime, get_academic_year, get_week_day


class TimeTable(APIView):
    '''
    获取时间表(目前只获取课程表)
    '''
    authentication_classes = [WeiXinAuth]

    @method_decorator(get_user_obj)
    def get(self, request, *args, **kwargs):

        res = BaseResponse()
        try:
            obj = kwargs.get('obj')
            if not obj:
                res.code = -1
                res.msg = '获取身份信息异常'
                return Response(res.get_dict)
            date = request.GET.get('date')

            if not date:
                res.code = -1
                res.msg = '请提供日期信息'
                return Response(res.get_dict)
            week = get_week_day(date)
            print(week)
            now_time = request.GET.get('time')
            school_id = settings.SCHOOL_ID
            # 获取开学日期
            starting_date = scmodels.SchoolCalendar.objects.filter(school_id=settings.SCHOOL_ID, date_des=1).first().date
            starting_date = date_to_datetime(starting_date)
            current_date = datetime.datetime.today()
            school_week, them = current_week(current_date, starting_date)
            # 获取年度信息
            year = ''
            if them:
                year = get_academic_year(them)
            base_q = Q()
            base_q.connector = "AND"
            base_q.children.append(('school_id', school_id))
            course_table_list = None
            res.data = {}
            if isinstance(obj, stumodels.StudentToParents):
                # 根据学生过滤日程信息
                student_obj = obj.student
                condition = Q()
                q1 = Q()
                q1.connector = "AND"
                q1.children.append(('stu_class', student_obj.stu_class))
                q1.children.append(('week', week))
                q2 = Q()
                q2.connector = "AND"
                q2.children.append(('info_type', 2))
                condition.add(q1, 'OR')
                condition.add(q2, 'OR')
                condition.add(base_q, 'AND')
                course_table_list = CourseTableService.get_table(condition, time=now_time)
                res.data['student_name'] = student_obj.full_name
            elif isinstance(obj, teamodels.TeacherInfo):
                teacher_obj = obj
                condition = Q()
                q1 = Q()
                q1.connector = "AND"
                q1.children.append(('week', week))
                q1.children.append(('teacher', teacher_obj))
                q1.children.append(('info_type', 2))
                condition.add(q1, 'OR')
                condition.add(base_q, 'AND')
                course_table_list = CourseTableService.get_table(condition)
            if not course_table_list:
                res.msg = '系统繁忙获取失败'
                res.code = -1
                return Response(res.get_dict)
            res.code = 200
            res.state = True
            res.data['them'] = them
            res.data['info'] = course_table_list
            res.data['year'] = year
            res.data['school_week'] = school_week
        except Exception as e:
            print(e)
            res.code = -1
            res.msg = "获取失败"
        return Response(res.get_dict)
