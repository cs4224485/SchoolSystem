import uuid
import datetime
import time


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
    d1 = datetime.date(y, m, d)
    timestamp = time.mktime(d1.timetuple())
    return (int((int(time.time() - timestamp)) / 86400))
