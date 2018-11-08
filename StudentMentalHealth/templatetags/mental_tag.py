from django import template
from utils.common import get_en_name
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