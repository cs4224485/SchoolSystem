import datetime
from django import template
from school import models
from utils.generate_calender import CalenderHandler
from utils.common import *

register = template.Library()


@register.inclusion_tag('setting/fields.html')
def fields():
    stu_info_choice = models.ChoiceField.objects.filter(field_type=1)
    hel_info_choice = models.ChoiceField.objects.filter(field_type=2)
    fam_info_choice = models.ChoiceField.objects.filter(field_type=3)
    par_info_choice = models.ChoiceField.objects.filter(field_type=4)
    customization_field = models.ChoiceField.objects.filter(field_type=5)
    return {'stu_info_choice': stu_info_choice,
            'hel_info_choice': hel_info_choice,
            'fam_info_choice': fam_info_choice,
            'par_info_choice': par_info_choice,
            'customization_field': customization_field,
            }


def generate_cal(calender_data, special_day, count=7):
    '''
    通过生成器生成日历每周7天
    :param calender_data:
    :param count:
    :return:
    '''

    calender_obj = CalenderHandler()
    current_day = datetime.datetime.today().date()
    for year, month in calender_data.items():
        for mon, days in month.items():
            index = 0
            # 每月第一天是周几
            first_day_of_mon = calender_obj.get_start_day(year, mon)
            # 只有在9月和1月时获取年
            the_year = ''
            if mon == 9 or mon == 1:
                the_year = year

            while True:
                # 每次返回一周的构建一个字典
                cal_dict = {
                    'day_list': [],
                    'is_new_month': False,
                    'mon': '',
                    'week': '',
                    'them': '',
                    'is_current': False,
                    'year': the_year,

                }

                # 如果index不是是0表示表示日期是当前月否则是一个新的月
                if index != 0:
                    day_list = days[index:index + count]
                    index += count
                else:
                    cal_dict['is_new_month'] = True
                    cal_dict['mon'] = mon
                    day_list = days[index:index + (count - first_day_of_mon + 1)]
                    for black in range(0, first_day_of_mon - 1):
                        day_list.insert(0, '')
                    index += index + (count - first_day_of_mon + 1)
                if not day_list:
                    break

                for day in day_list:
                    # 处理一周日程每一天的情况
                    cn_day = ''
                    day_dict = {}
                    if day:
                        temp_day = datetime.datetime.strptime('%s-%s-%s' % (year, mon, day), '%Y-%m-%d')
                        cn_day = calender_obj.getCnDay(temp_day)
                        cn_month = calender_obj.getCnMonth(temp_day)
                        holiday = calender_obj.get_pub_holiday(mon, day) if calender_obj.get_pub_holiday(mon, day) else calender_obj.get_cn_holiday(cn_month, cn_day)
                        if holiday:
                            day_dict['holiday'] = holiday
                        if cn_day == '初一':
                            cn_day = cn_month
                        if current_day == temp_day.date():
                            cal_dict['is_current'] = True
                        # 处理学校特殊日期
                        if temp_day.date() in special_day:
                            special_data = special_day[temp_day.date()]
                            end_date = special_data.get('end_date')
                            if end_date and temp_day.date() < end_date:
                                special_day.pop(temp_day.date())
                                special_day[temp_day.date()+datetime.timedelta(days=1)] = special_data
                                day_dict['end_date'] = end_date
                            day_dict['special_day'] = special_data.get('des')
                            day_dict['special_id'] = special_data.get('id')
                            day_dict['des_id'] = special_data.get('des_id')
                        if day == day_list[-1]:
                            # 用本周的最后一天去判断学校周次
                            school_week = current_week(temp_day)
                            # 如果是新的一个月并且1号是周一就不显示第X周了
                            if cal_dict['is_new_month'] and '' in day_list:
                                cal_dict['week'] = ''
                            elif school_week:
                                cal_dict['week'] = school_week[0]
                    day_dict['day'] = day
                    day_dict['cn_day'] = cn_day
                    cal_dict['day_list'].append(day_dict)
                yield cal_dict


@register.inclusion_tag('school_info/cal_table.html')
def ger_cal(calender_data, special_day):
    '''
    生成日历
    :param calender_data:
    :param special_day:
    :return:
    '''

    current_day = datetime.datetime.today().day
    return {'cal': generate_cal(calender_data, special_day), 'today': current_day}
