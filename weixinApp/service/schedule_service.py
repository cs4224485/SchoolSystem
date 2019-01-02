from school import models as scmodels
from django.db.models import Q


class CourseTableService(object):
    @staticmethod
    def get_table(q_condition, time=None):
        '''
        根据条件过滤课程表
        :param q_condition:
        :return:
        '''
        if time:
            add_q = Q()
            add_q.children.append(('time_range__gte', time))
            q_condition.add(add_q, 'AND')

        course_table_queryset = scmodels.SchoolTimetable.objects.filter(q_condition)
        course_table_list = []
        for item in course_table_queryset:
            if item.info_type == 1:
                stu_class = item.stu_class.name
                grade = item.stu_class.grade.get_grade_name_display()
                course_table_list.append({'id': item.id, 'des': item.course.course_des,
                                          'teacher': item.teacher.last_name + item.teacher.first_name,
                                          'time': item.time_range, 'type': '上课', '_class': '%s%s' % (grade, stu_class)})
            else:
                course_table_list.append(
                    {'id': item.id, 'des': item.get_other_event_display(), 'time': item.time_range, 'teacher': '',
                     "type": '活动'})

        return course_table_list
