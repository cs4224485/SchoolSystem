from django import template
from utils.common import get_en_name
from utils.common import current_week
import datetime
register = template.Library()


@register.inclusion_tag('head_info.html')
def head_stu_info(student_obj):
    '''
    学生头部信息
    :param stu_obj:
    :return:
    '''
    # 姓名转换成拼音
    en_name = get_en_name(student_obj.full_name)
    return {'student': student_obj, 'en_name':en_name}

@register.simple_tag()
def trance_week(date):
    print(date, 'date')
    weeks = ((1, '周一'), (2, '周二'), (3, '周三'), (4, '周四'), (5, '周五'), (6, '周六'), (7, '周日'))
    week = datetime.datetime.strptime(str(date), '%Y-%m-%d').weekday()
    return weeks[week][1]

@register.simple_tag()
def get_school_week(date):
    date = datetime.datetime.strptime(str(date), '%Y-%m-%d')
    school_week = current_week(date)
    return '%s第%s周' % (school_week[1], school_week[0])