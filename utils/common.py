import uuid
import datetime
import time
import re
import hashlib
import random
from pypinyin import lazy_pinyin


def create_uuid():
    random_id = uuid.uuid4()
    return random_id


def get_constellation(month, date):
    '''
    根据生日计算星座
    :param month:
    :param date:
    :return:
    '''
    print(month, date, '000000')
    dates = (21, 20, 21, 21, 22, 22, 23, 24, 24, 24, 23, 22)
    constellations = (
        (1, "摩羯"), (2, "水瓶"), (3, "双鱼"), (4, "白羊"), (5, "金牛"), (6, "双子"), (7, "巨蟹"), (8, "狮子"), (9, "处女"), (10, "天秤"),
        (11, "天蝎"), (12, "射手"), (1, "摩羯"))
    if date < dates[month - 1]:
        return constellations[month - 1]
    else:
        return constellations[month]


def get_ChineseZodiac(year):
    '''
    根据生日计算生肖
    :param year:
    :return:
    '''

    return ((1, '猴'), (2, '鸡'), (3, '狗'), (4, '猪'), (5, '鼠'),
            (6, '牛'), (7, '虎'), (8, '兔'), (9, '龙'), (10, '蛇'), (11, '马'), (12, '羊'))[year % 12]


def calculate_age(born):
    '''
    根据生日计算年龄
    :param born:
    :return:
    '''
    this_year = str(datetime.datetime.now().year)
    age = int(this_year) - born
    return str(age)


def calculate_day_age(y, m, d):
    '''
    计算日龄
    :param y:
    :param m:
    :param d:
    :return:
    '''
    d1 = datetime.date(y, m, d)
    timestamp = time.mktime(d1.timetuple())
    return (int((int(time.time() - timestamp)) / 86400))


def calculate_info(birthday):
    '''
    根据生日计算信息
    :param birthday:
    :return:
    '''
    try:
        if birthday:
            y, m, d = birthday.split('-')
            constellations = get_constellation(int(m), int(d))
            ChineseZodiac = get_ChineseZodiac(int(y))
            age = calculate_age(int(y))
            day_age = calculate_day_age(int(y), int(m), int(d))
            return {'constellations': constellations[0], 'ChineseZodiac': ChineseZodiac[0], 'age': age,
                    'day_age': day_age}
    except Exception:
        return None


def calculate_period(grade):
    '''
    根据年级计算届别
    :param grade:
    :return:
    '''
    grade_choice = (
        '一年级', '二年级', '三年级', '四年级', '五年级', '六年级', '初一', '初二', '初三', '高一', '高二', '高三')

    if grade in grade_choice:
        grade_index = grade_choice.index(grade)
        if datetime.date.today().month >= 9:
            period = datetime.date.today().year - grade_index
        else:
            period = datetime.date.today().year - grade_index - 1
        return period


def get_en_name(name):
    '''
    获取英文名字
    :param name:
    :return:
    '''
    pinyin_name = lazy_pinyin(name)
    last_name = pinyin_name[0]
    first_name_list = pinyin_name[1:]
    first_name = ""
    for y in first_name_list:
        first_name += y
    en_name = last_name + " " + first_name
    en_name = en_name.title().lstrip()

    return en_name


def school_calendar(date, starting_date=None):
    '''
    获取校历
    :return:
    '''
    current_year = datetime.datetime.today().year
    special_mon = (1, 2)
    year = date.year
    if date.month in special_mon:
        year = int(date.year - 1)
        date = date - datetime.timedelta(days=365)
    first_them_range = [datetime.datetime.strptime('%s-9-3' % year, '%Y-%m-%d'),
                        datetime.datetime.strptime('%s-2-19' % year, '%Y-%m-%d')]

    if date.month >= 9 or date < first_them_range[1]:
        them = '第一学期'
        start_time = first_them_range[0]
    else:
        them = '第二学期'
        if date.month in special_mon:
            year += 1
            first_them_range[1] = datetime.datetime.strptime('%s-2-19' % year, '%Y-%m-%d')
        start_time = first_them_range[1]
    if starting_date:
        start_time = starting_date

    time_range = []
    for i in range(1, 23):
        time_range.append(start_time)
        start_time = start_time + datetime.timedelta(weeks=1)

    return time_range, them


def current_week(current_date, starting_date=None):
    '''
    根据当前时间获取周次
    :param current_date:  当前日期
    :param starting_date: 开学日期
    :return:
    '''
    time_range, them = school_calendar(current_date, starting_date)
    for index, time in enumerate(time_range, start=0):
        try:
            if current_date >= time_range[index] and current_date < time_range[index + 1]:
                return index + 1, them
            else:
                continue
        except Exception as e:
            return '', ''


def get_academic_year(them):
    '''
    获取学年信息
    :param them:
    :return:
    '''
    if them == '第一学期':
        special_mon = (1, 2)
        current_mon = datetime.datetime.now().month
        if current_mon in special_mon:
            year = [datetime.datetime.today().year - 1, datetime.datetime.today().year]
        else:
            year = [datetime.datetime.today().year, datetime.datetime.today().year + 1]
    else:
        year = [datetime.datetime.today().year - 1, datetime.datetime.today().year]

    academic_year = '%s-%s年度' % (year[0], year[1])

    return academic_year


def date_to_datetime(date, date_format='%Y-%m-%d'):
    '''
    date对象转成datetime
    :param date:
    :param date_format:
    :return:
    '''

    datetime_obj = datetime.datetime.strptime(str(date), date_format)
    return datetime_obj


def get_week_day(date, date_format='%Y-%m-%d'):
    '''
    根据日期判断周几
    :param date:
    :param date_format:
    :return:
    '''
    week = datetime.datetime.strptime(date, date_format).weekday() + 1
    return week


def shadow_name(first_name, last_name):
    '''
    处理姓名加*号显示
    :param first_name:
    :param last_name:
    :return:
    '''
    if len(first_name) > 1:
        first_name = first_name[-1]
        mark = '*'
        mark *= len(first_name) - 1
        return first_name, last_name, mark
    return first_name, last_name, '*'


def order_by_class(class_list):
    '''
    对班级名称进行排列，使用冒泡算法
    :param class_list:
    :return:
    '''
    regx = '\d+'
    for i in range(0, len(class_list)):
        exchange = False
        for j in range(0, len(class_list) - i - 1):
            # 如果届别（年级）不相对无需进行比较
            period_j = calculate_period(class_list[j].grade.get_grade_name_display())
            period_next = calculate_period(class_list[j+1].grade.get_grade_name_display())
            if period_j != period_next:
                continue
            match_class_num = re.search(regx, class_list[j].name)
            match_next_class_num = re.search(regx, class_list[j + 1].name)
            if match_class_num and match_next_class_num:
                this_class_num = int(match_class_num.group())
                next_class_num = int(match_next_class_num.group())
                if this_class_num > next_class_num:
                    class_list[j], class_list[j + 1] = class_list[j + 1], class_list[j]
                    exchange = True
        if not exchange:
            return class_list
    return class_list


def gen_md5_password(password):
    """
       md5加密time
       :param password: 输入的密码
       :return:
       """
    ha = hashlib.md5(b'jk3usodfjwkrsdf')
    ha.update(password.encode('utf-8'))
    return ha.hexdigest()

