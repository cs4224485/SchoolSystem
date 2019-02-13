import datetime
import json
from school import models
from django.db.models import Q
from utils.common import get_academic_year, calculate_period, current_week, order_by_class
from collections import OrderedDict


class CourseService(object):
    '''
    课程表相关信息的操作
    '''

    def __init__(self, school_id, grade):
        self.school_id = school_id
        self.grade = grade
        self.school_obj = models.SchoolInfo.objects.filter(id=school_id).only('school_name').first()
        self.grade_obj = models.Grade.objects.filter(id=grade).first()
        self.grade_display = self.grade_obj.get_grade_name_display()

    def _get_school_head(self):
        '''
        构建学校头部信息
        :return:
        '''
        them = current_week(datetime.datetime.today())[1]
        table_year = get_academic_year(them)
        period = calculate_period(self.grade_display)
        head_info_dict = {
            'school_name': self.school_obj.school_name,
            'grade': self.grade_display,
            'period': period,
            'year': table_year,
        }

        return head_info_dict

    def _get_course_list(self):
        '''
        获取学校教学层次获取课程信息
        :return:
        '''
        layer = self.school_obj.school_layer
        course_queryset = []
        if not layer:
            course_queryset = models.Course.objects.all()
            return course_queryset
        if layer == 2:
            course_queryset = models.Course.objects.filter(period__in=[1, 3])
        elif layer == 3 or layer == 4:
            course_queryset = models.Course.objects.filter(period__in=[2, 3])
        elif layer != 1:
            course_queryset = models.Course.objects.all()

        return course_queryset

    def _get_other_event(self):
        '''
        获取学校其他课间项目
        :return:
        '''

        other_event = models.SchoolTimetable.other_event_choice
        return other_event

    def _get_course_data(self):
        '''
        获取学校课程数据
        :return:
        '''

        course_table_queryset = models.SchoolTimetable.objects.filter(
            Q(stu_class__grade_id=self.grade, school=self.school_obj) |
            Q(school=self.school_obj, info_type=2)).order_by('time_range', 'week')

        per_grade_time = []
        course_time_dict = {}
        # 构建每个时间点包含的course对象
        for item in course_table_queryset:
            time_key = datetime.time.strftime(item.time_range.start_time, '%H:%M')
            per_grade_time.append(time_key)
            if time_key not in course_time_dict:
                course_time_dict[time_key] = [item]
            else:
                course_time_dict[time_key].append(item)
        all_time_range = self._get_time_range()

        # 构建课程信息字典
        course_table_dict = OrderedDict()
        for time in all_time_range:
            if time not in per_grade_time:
                course_table_dict[time] = {}
                continue
            for table_item in course_time_dict.get(time):
                key = datetime.time.strftime(table_item.time_range.start_time, '%H:%M')
                if table_item.other_event:
                    node = {
                        'course_table_id': table_item.id,
                        'is_event': True,
                        'other_event': table_item.get_other_event_display(),
                        'event_id': table_item.other_event
                    }
                else:
                    node = {'course_table_id': table_item.id,
                            'course_id': table_item.course.id,
                            'course': table_item.course.course_des,
                            'teacher_id': table_item.teacher.id,
                            'teacher': table_item.teacher.last_name + table_item.teacher.first_name,
                            'week': table_item.week,
                            'class_id': table_item.stu_class_id,
                            'position': table_item.position,
                            'is_event': False,
                            }
                    if table_item.single_double_week != 1:
                        node['week_info'] = table_item.single_double_week
                if key not in course_table_dict:
                    course_table_dict[key] = [node]
                else:
                    course_table_dict[key].append(node)
        return course_table_dict

    def _get_time_range(self):
        '''
        获取学校时间课程时间段
        :return:
        '''
        course_time_queryset = models.SchoolTimeRange.objects.filter(school=self.school_obj).values_list(
            'start_time').distinct().order_by('start_time')

        course_time_list = []
        for item in course_time_queryset:
            course_time_list.append(datetime.time.strftime(item[0], '%H:%M'))
        return course_time_list

    def create_course_data(self):
        '''
        构建课程表页面需要的数据
        :return:
        '''

        class_list = order_by_class(list(models.StuClass.objects.filter(grade_id=self.grade, school_id=self.school_id)))
        week_list = [1, 2, 3, 4, 5]
        course_list = self._get_course_list()
        other_event = self._get_other_event()
        head_info = self._get_school_head()
        grad_queryset = models.StuClass.objects.filter(school=self.school_obj).select_related('grade').values(
            'grade__grade_name', 'grade_id').distinct()
        # 生成年级信息
        for item in grad_queryset:
            item['grade__grade_name'] = models.Grade.grade_choice[item['grade__grade_name'] - 1][1]
        course_table_dict = json.dumps(self._get_course_data(), ensure_ascii=False)
        selected_grade = models.Grade.objects.filter(id=self.grade).first()

        data_dict = {
            'class_list': class_list,
            'week_list': week_list,
            'course_list': course_list,
            'other_event': other_event,
            'head_info': head_info,
            'grad_queryset': grad_queryset,
            'course_table_dict': course_table_dict,
            'selected_grade': selected_grade,
        }

        return data_dict
