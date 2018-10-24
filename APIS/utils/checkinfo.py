from students.models import *
import re
import datetime


def check_id_exist(id_card):
    '''
    校验输入的身份证在数据库是否存在
    :param id_card:
    :return:
    '''
    student = StudentInfo.objects.filter(id_card=id_card)
    if student:
        return True


def check_id_card(id_number):
    info = {
        'birthday': '',
        'gender': '',
        'msg': '验证通过',
    }

    id_code_list = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
    check_code_list = [1, 0, 'X', 9, 8, 7, 6, 5, 4, 3, 2]
    if len(id_number) != 18:
        info['msg'] = "身份证长度错误"
        return False, info
    if not re.match(r"^\d{17}(\d|X|x)$", id_number):
        info['msg'] = "身份证格式错误"
        return False, info
    # if id_number[0:6] not in area_dict:
    #     return False, "身份证区域信息错误"
    try:
        birthday = datetime.date(int(id_number[6:10]), int(id_number[10:12]), int(id_number[12:14]))
    except ValueError as ve:
        info['msg'] = "身份证号码出生日期超出范围或含有非法字符"
        return False, info
    # 校验最后一位
    if str(check_code_list[sum([a * b for a, b in zip(id_code_list, [int(a) for a in id_number[0:-1]])]) % 11]) != str(id_number.upper()[-1]):
        info['msg'] = "身份证号码校验错误!"
        return False, info
    # 判断男女

    gender = (1, '男') if int(id_number[-2]) % 2 == 1 else (2, '女')

    info['birthday'] = str(birthday)
    info['gender'] = gender
    return True, info

