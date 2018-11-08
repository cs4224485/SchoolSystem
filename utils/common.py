import uuid
import datetime
import time
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


def calculate_period(grade):
    '''
    根据年级计算届别
    :param grade:
    :return:
    '''
    grade_choice = (
     '一年级',  '二年级',  '三年级',  '四年级',  '五年级',  '六年级',  '初一',  '初二',  '初三', '高一',  '高二',  '高三')
    if grade in grade_choice:
        grade_index = grade_choice.index(grade)
        if datetime.date.today().month >= 9:
            period = datetime.date.today().year - grade_index
        else:
            period = datetime.date.today().year - grade_index + 1
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


def school_calendar():
    '''
    获取校历
    :return:
    '''
    current_year = str(datetime.datetime.now().year)
    current_month = datetime.datetime.now().month
    if current_month >= 9:
        them = '第一学期'
        start_time = datetime.datetime.strptime('%s-9-1' % current_year, '%Y-%m-%d')
    else:
        them = '第二学期'
        start_time = datetime.datetime.strptime('%s-2-19' % current_year, '%Y-%m-%d')
    time_range = []
    for i in range(1, 23):
        time_range.append(start_time)
        start_time = start_time + datetime.timedelta(weeks=1)

    return time_range, them


def current_week(current_date):
    '''
    根据当前时间获取周次
    :param current_date:
    :return:
    '''
    time_range, them = school_calendar()
    for index, time in enumerate(time_range, start=1):
        try:
            if current_date >= time_range[index] and current_date <= time_range[index + 1]:
                return index + 1, them
            else:
                continue
        except Exception as e:
            print(e)
            return len(time_range), them