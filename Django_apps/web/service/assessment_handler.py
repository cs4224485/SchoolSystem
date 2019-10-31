#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/7/15'
import xlrd
import datetime
import uuid
from utils.file_handler import ExcelUploadHandler
from Django_apps.students import models
from school.models import SchoolInfo, StuClass, Grade
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor
from utils.common import calculate_day_age
from django.db.models import Q

GENDER_MAP = {'男': 1, '女': 2}
GRADE_MAP = {'小班': 13, '中班': 14}
CHOICE_MAP = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5}
# excel每页标题与类方法的映射
PAGE_FUN_MAP = {
    "儿童测前基本状况调查表": "base_info",
    "大运动": "sport",
    "语言表达": "language",
    "观察与评估记录": "observe",
    "精细动作": "action",
    "语言理解": "language_comprehension",
    "联想": "associate",
    "数的认知": "cognition_of_number",
    "逻辑思维": "logic",
    "持续注意": "attention",
    "短时记忆": "short_memory",
    "科学常识": "science",
    "生活常识": "life",
    "生活习惯和卫生习惯": "habits_of_life",
    "安全意识": "safety_consciousness",
    "社会": "society",
    "艺术素养": "art",
    "兴趣爱好": "interest"
}


class AssessmentHandler(object):
    '''
    处理综合评估源数据的处理
    '''

    def __init__(self, request):
        self.request = request
        self.excel = ExcelUploadHandler(file=self.request.FILES.get("import_excel"))

    def import_source_data(self):
        workbook = self.excel.open_excel()
        self.get_per_sheet(workbook)

    def get_per_sheet(self, workbook):
        '''
        循环Excel中每一页数据
        :param workbook:
        :return:
        '''
        pool = self.__create_thread_pool()
        grade = None
        for index, sheet_name in enumerate(workbook.sheet_names()):
            try:
                sheet = workbook.sheet_by_index(index)
                if index == 0:
                    grade = sheet.row(1)[6].value
                # 确保每页描述对应到相应的函数执行
                fun_str = PAGE_FUN_MAP.get(sheet_name)
                if fun_str:
                    if hasattr(self, fun_str):
                        fun = getattr(self, fun_str)
                        pool.submit(fun, sheet, grade=grade)
                        # fun(sheet, grade=grade)
            except IndexError as e:
                print(e)
                continue

    def base_info(self, sheet, *args, **kwargs):
        '''
        基础信息的导入
        :param sheet:
        :return:
        '''
        row_map = {
            0: {'text': '姓名', 'name': 'full_name'},
            1: {'text': '姓', 'name': 'first_name'},
            2: {'text': '名', 'name': 'last_name'},
            3: {'text': '性别', 'name': 'gender'},
            4: {'text': '出生日期', 'name': 'birthday'},
            5: {'text': '幼儿园名称', 'name': "school"},
            6: {'text': '年级', 'name': 'grade'},
            7: {'text': '班级', 'name': '_class'},
            8: {'text': '测试时间', 'name': 'test_time'},
            9: {'text': '测试内容', 'name': 'test_content'},
            10: {'text': '优势手', 'name': 'dominant_hand'},
            11: {'text': '身体与情绪', 'name': "emotion"},
            12: {'text': '说明', 'name': 'memo'}
        }
        ignore_col = (1, 2, 3, 4, 5, 6, 7)
        object_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)
            row_dict = {}
            student_obj = None
            for col_num, name_text in row_map.items():
                if col_num == 0:
                    school_obj = self.check_school(row[5].value)
                    first_name = row[2].value
                    last_name = row[1].value
                    gender = GENDER_MAP.get(row[3].value)
                    cell = sheet.cell_value(row_num, col_num + 4)

                    birthday = self.excel.trans_datetime(cell).date()
                    grade = GRADE_MAP.get(row[6].value)
                    _class = row[7].value
                    student_obj = self.check_student(first_name, last_name, birthday, school_obj, grade, gender, _class)
                    row_dict['school'] = school_obj
                    row_dict['student'] = student_obj
                    continue
                elif col_num == 8:
                    excel_time = row[8].value
                    test_time = None
                    if excel_time:
                        test_time = self.excel.trans_datetime(row[8].value)
                    row_dict['test_time'] = test_time
                    continue
                if col_num in ignore_col: continue
                row_dict[name_text['name']] = None if row[col_num].value == '' else row[col_num].value
            test_time = datetime.datetime(*xlrd.xldate_as_tuple(row[8].value, 0))
            try:
                obj = models.QualityAssessmentSource.objects.get(student=student_obj, test_time=test_time)
            except models.QualityAssessmentSource.DoesNotExist as e:
                print(e)
                object_list.append(models.QualityAssessmentSource(**row_dict))
        models.QualityAssessmentSource.objects.bulk_create(object_list)

    def sport(self, sheet, *args, **kwargs):
        '''
        大运动
        :param sheet:
        :return:
        '''
        # row_map = {
        #     3: {'text': '抛球-第一次', 'name': 'boole_answer', 'dimension': 1, 'number': 1},
        #     4: {'text': '抛球-第二次', 'name': 'boole_answer', 'dimension': 1, 'number': 2},
        #     5: {'text': '抛球-第三次', 'name': 'boole_answer', 'dimension': 1, 'number': 3},
        #     6: {'text': '单手丢沙包-第一次', 'name': 'boole_answer', 'dimension': 1, 'number': 4},
        #     7: {'text': '单手丢沙包-第二次', 'name': 'boole_answer', 'dimension': 1, 'number': 5},
        #     8: {'text': '单手丢沙包-第三次', 'name': 'boole_answer', 'dimension': 1, 'number': 6},
        #     9: {'text': '直线走-第一次', 'name': 'boole_answer', 'dimension': 2, 'number': 7},
        #     10: {'text': '直线走-第二次', 'name': 'boole_answer', 'dimension': 2, 'number': 8},
        #     11: {'text': '直线走-第三次', 'name': 'boole_answer', 'dimension': 2, 'number': 9},
        #     12: {'text': '单脚行进跳-第一次', 'name': 'boole_answer', 'dimension': 2, 'number': 10},
        #     13: {'text': '单脚行进跳-第二次', 'name': "boole_answer", 'dimension': 2, 'number': 11},
        #     14: {'text': '单脚行进跳-第三次', 'name': 'boole_answer', 'dimension': 2, 'number': 12},
        #     15: {'text': '15米折返跑-第一次', 'name': 'float_score', 'dimension': 3, 'number': 13},
        #     16: {'text': '15米折返跑-第二次', 'name': 'float_score', 'dimension': 3, 'number': 14},
        #     17: {'text': '15米折返跑-第三次', 'name': 'float_score', 'dimension': 3, 'number': 15},
        #     18: {'text': '特殊问题1', 'name': 'boole_answer', 'dimension': 4, 'number': 16},
        #     19: {'text': '特殊问题2', 'name': 'boole_answer', 'dimension': 4, 'number': 17},
        #     20: {'text': '特殊问题3', 'name': 'boole_answer', 'dimension': 4, 'number': 18},
        #     21: {'text': '特殊问题4', 'name': 'boole_answer', 'dimension': 4, 'number': 19},
        #     22: {'text': '特殊问题5', 'name': 'boole_answer', 'dimension': 4, 'number': 20},
        #     23: {'text': '特殊问题6', 'name': 'boole_answer', 'dimension': 4, 'number': 21},
        # }
        col_type_dict = {'float_score': (15, 16, 17)}
        dimension_dict = {
            1: (3, 4, 5, 6, 7, 8),
            2: (9, 10, 11, 12, 13, 14),
            3: (15, 16, 17),
            4: (18, 19, 20, 21, 22, 23),
        }
        self.__unify_2_db_interface(sheet, "sport", col_type_dict=col_type_dict, dimension_dict=dimension_dict)

    def language(self, sheet, *args, **kwargs):
        '''
        语言表达
        :param sheet:
        :return:
        '''
        self.__unify_2_db_interface(sheet, "language")

    def observe(self, sheet, *args, **kwargs):
        '''
        观察与评估记录
        :param sheet:
        :return:
        '''
        # DB维度映射字段

        dimension_dict = {
            5: (3, 4, 5),  # 安全意识和自我保护
            6: (6, 7, 8, 24, 25, 26, 30, 31, 32),  # 安定情绪
            7: (9, 10, 11, 12, 13, 14),  # 规则意识
            8: (15, 16, 17, 36, 37, 38),  # 情绪识别
            9: (18, 19, 20),  # 群体生活
            10: (21, 22, 23, 33, 34, 35),  # 适应能力
            11: (27, 28, 29)  # 倾听与表达
        }
        self.__unify_2_db_interface(sheet, "observe", dimension_dict=dimension_dict)

    def action(self, sheet, *args, **kwargs):
        '''
        精细动作
        :param sheet:
        :return:
        '''

        col_type_dict = {'score_answer': (3, 4, 5, 6), }

        dimension_dict = {
            12: (3, 4, 5, 6),
            13: (7, 8, 13, 14, 15),
            14: (9, 10, 11, 12),
            15: (16, 17, 18, 19, 20, 21)
        }

        self.__unify_2_db_interface(sheet, "action", col_type_dict=col_type_dict, dimension_dict=dimension_dict)

    def language_comprehension(self, sheet, *args, **kwargs):
        '''
        语言理解
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "language_comprehension", col_type_dict=col_type_dict)

    def associate(self, sheet, *args, **kwargs):
        '''
        联想
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "associate", col_type_dict=col_type_dict)

    def cognition_of_number(self, sheet, *args, **kwargs):
        '''
        数的认知
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "cognition_of_number", col_type_dict=col_type_dict)

    def logic(self, sheet, *args, **kwargs):
        '''
        逻辑
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "logic", col_type_dict=col_type_dict)

    def attention(self, sheet, *args, **kwargs):
        '''
        持续注意
        :param sheet:
        :return:
        '''
        self.__unify_2_db_interface(sheet, "attention")

    def short_memory(self, sheet, *args, **kwargs):
        '''
        短时记忆
        :param sheet:
        :return:
        '''
        self.__unify_2_db_interface(sheet, "short_memory")

    def science(self, sheet, *args, **kwargs):
        '''
        科学
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "science", col_type_dict=col_type_dict)

    def life(self, sheet, *args, **kwargs):
        '''
        生活常识
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "life", col_type_dict=col_type_dict)

    def habits_of_life(self, sheet, *args, **kwargs):
        '''
        生活习惯和卫生习惯
        :param sheet:
        :return:
        '''

        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        self.__unify_2_db_interface(sheet, "habits_of_life", col_type_dict=col_type_dict)

    def safety_consciousness(self, sheet, *args, **kwargs):
        '''
        安全意识
        :param sheet:
        :return:
        '''

        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        # 小班与中班维度对应字段不一样, 默认是的小班
        dimension_dict = {
            16: (3, 5),
            17: (4,),
        }
        grade = kwargs.get("grade")
        if grade == "中班":

            dimension_dict = {
                16: (3, 4),  # 自理能力
                17: (5,),  # 安全意识和自我保护
            }
        self.__unify_2_db_interface(sheet, "safety_consciousness", col_type_dict=col_type_dict,
                                    dimension_dict=dimension_dict)

    def society(self, sheet, *args, **kwargs):
        '''
        社会
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        grade = kwargs.get("grade")
        dimension_dict = {
            18: (3, 4, 13),
            19: (5, 6, 11, 14),
            20: (7, 12,),
            21: (8, 9, 10),
        }

        if grade == "中班":
            dimension_dict = {
                18: (3, 4, 5, 9, 10),  # 群体生活
                19: (12, 13, 14, 15, 16),  # 规则意识
                20: (7,),  # 自主表现
                21: (6, 8, 11)  # 尊重他人
            }

        self.__unify_2_db_interface(sheet, "society", col_type_dict=col_type_dict, dimension_dict=dimension_dict)

    def art(self, sheet, *args, **kwargs):
        '''
        艺术素养
        :param sheet:
        :return:
        '''
        col_type_dict = {"choice_question": [i for i in range(3, sheet.ncols)]}
        dimension_dict = {
            22: (3, 4, 5, 6),  # 感受与欣赏
            23: (7, 8),  # 表现与创造
        }
        grade = kwargs.get("grade")
        if grade == "中班":
            dimension_dict[22] = (3, 4, 5, 6, 9, 10, 11)
        self.__unify_2_db_interface(sheet, "art", col_type_dict=col_type_dict, dimension_dict=dimension_dict)

    def interest(self, sheet, *args, **kwargs):
        '''
        兴趣爱好
        :param sheet:
        :return:
        '''

        dimension_dict = {
            24: (3, 4, 5),
            25: (6, 7, 8),
            26: (9, 10, 11),
            27: (12, 13, 14),
            28: (15, 16, 17),
            29: (18, 19, 20),
            30: (21, 22, 23),
            31: (24, 25, 26)
        }
        self.__unify_2_db_interface(sheet, "interest", dimension_dict=dimension_dict)

    def __unify_2_db_interface(self, sheet, level_1_dimension, col_type_dict=None, dimension_dict=None):
        '''
        将每个sheet需要调用的方法统一封装， 每个sheet调用次方法即可
        :param sheet:
        :param col_type_dict:
        :param dimension_dict:
        :return:
        '''
        row_map = self.__create_row_map(sheet)
        if col_type_dict:
            self.__create_col_type_2_db(col_type_dict, row_map)
        else:
            self.__col_to_db_col([], row_map)

        if dimension_dict:
            self.__create_dimension_map(dimension_dict, row_map)
        self.__create_answer_2_db(sheet, row_map, level_1_dimension)

    def __col_to_db_col(self, col_list, row_map, col_type='boole_answer'):
        '''
        把Excel获取到值对应到数据存储值得类型
        比如是浮点类型得字段就在row_map 标识为 float_score, 布尔就标识为： boole_answer
        由于布尔类型所占比例较多所以默认就是布尔类型
        :return:
        '''
        for col_num, col_dic in row_map.items():
            if col_num in col_list:
                row_map[col_num]['name'] = col_type
            else:
                row_map[col_num]['name'] = 'boole_answer'

    def __create_col_type_2_db(self, col_dict, row_map):
        '''
        根据excel不同的类型对应到数据库相应的数据类型
        :param col_dict:
        :param row_map:
        :return:
        '''

        for col_type, col_nums in col_dict.items():
            self.__col_to_db_col(col_nums, row_map, col_type=col_type)

    def __create_dimension_map(self, dimension_dict, row_map):
        '''
        创建二级维度映射
        :param dimension_dict:每个一级维度的二级维度与字段映射字典
        :param row_map:
        :return:
        '''
        for dimension, cols in dimension_dict.items():
            self.__map_dimension(cols, row_map, dimension)

    def __map_dimension(self, col_list, row_map, dimension):
        '''
        映射每个字段所对应得数据库维度
        :param col_list:
        :param rom_map:
        :param dimension:
        :return:
        '''

        for col_num, col_dic in row_map.items():
            if col_num in col_list:
                row_map[col_num]['dimension'] = dimension

    def __create_row_map(self, sheet, ignore_col=2):
        '''
        创建excl列映射字典
        例如：
            3: {'text': '抛球-第一次',  'number': 1},
            4: {'text': '抛球-第二次',  'number': 2},
            5: {'text': '抛球-第三次',  'number': 3},
            6: {'text': '单手丢沙包-第一次',  'number': 4},
            7: {'text': '单手丢沙包-第二次',  'number': 5},
            8: {'text': '单手丢沙包-第三次',  'number': 6},
        :param sheet:
        :param ignore_col:
        :return:
        '''
        # 获取Excel列数
        cols_count = sheet.ncols
        row_map = {}
        for rol_col in range(1, cols_count):
            col_num = rol_col + ignore_col
            if col_num >= cols_count:
                break
            col_value = sheet.cell(0, col_num).value
            row_dict = {col_num: {"text": col_value, 'number': rol_col}}

            row_map.update(row_dict)
        return row_map

    def __create_answer_2_db(self, sheet, row_map, level_1_dimension):
        '''
        创建答题源数据到数据库
        :param sheet:
        :param row_map: 与excel映射的字典
        :param level_1_dimension:一级维度
        :return:
        '''
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)
            name = row[0].value
            ass_obj = self.__get_assessment_obj(name)

            if not ass_obj: continue
            answer_list = []
            for col_num, col_dic in row_map.items():
                value = self.__parse_none_value(row[col_num].value)

                if col_dic['name'] == "boole_answer":
                    value = self.__parse_boole(value)
                if col_dic['name'] == 'score_answer':
                    value = int(value) if value else None
                if col_dic['name'] == 'choice_question':
                    value = self.__parse_choice(value)
                if col_dic['name'] == 'float_score':
                    value = value if value else None
                data_dict = {
                    col_dic['name']: value,
                    'number': col_dic['number'],
                    'level_1_dimension': level_1_dimension,
                    'excel_col_des': col_dic['text']
                }
                if col_dic.get("dimension", None) is not None:
                    data_dict['level_2_dimension'] = col_dic['dimension']
                try:
                    obj = models.Answers.objects.get(assessment=ass_obj, number=col_dic['number'],
                                                     level_1_dimension=level_1_dimension)
                except models.Answers.DoesNotExist as e:
                    print(e)
                    answer_obj = models.Answers(assessment=ass_obj, **data_dict)
                    answer_list.append(answer_obj)
            models.Answers.objects.bulk_create(answer_list, batch_size=200)

    def __parse_none_value(self, value):
        '''
        解析空字段
        :param value:
        :return:
        '''
        if value == '' or value == "--":
            return None
        return value

    def __parse_boole(self, value):
        '''
        解析布尔类型 表中填写的内容与True和False的映射
        :param value:
        :return:
        '''
        # true
        BT = ('T', 'Y', '可以', '1', 1)
        # FALSE
        BF = ('N', 'F', '0')
        if value in BT:
            return True
        elif value in BF:
            return False
        return None

    def __parse_choice(self, value):
        '''
        解析选择问题
        :param value:
        :return:
        '''
        if value in CHOICE_MAP:
            return CHOICE_MAP[value]

    def __get_assessment_obj(self, student_name):
        '''
        获取评测基础信息表对象
        :param student_name:
        :return:
        '''
        obj = models.QualityAssessmentSource.objects.filter(student__full_name=student_name).first()
        return obj

    def check_school(self, school_name, school_layer=1):
        '''
        检查学校是否存在
        :param school_name:
        :param school_layer:
        :return:
        '''
        school_obj = SchoolInfo.objects.filter(school_name=school_name).first()
        if not school_obj:
            school_obj = SchoolInfo.objects.create(school_name=school_name, school_layer=school_layer,
                                                   internal_id=uuid.uuid4())
            for g in settings.SCHOOL_GRADE_MAPPING[school_layer]:
                grade = Grade.objects.filter(grade_name=g).first()
                StuClass.objects.create(grade=grade, school=school_obj, name="1班")
        return school_obj

    def check_student(self, first_name, last_name, birthday, school_obj, grade, gender, _class):
        '''
        检查学生是否存在
        :param first_name:
        :param last_name:
        :param birthday:
        :param school_obj:
        :param grade:
        :return:
        '''
        name = last_name + first_name
        student_obj = models.StudentInfo.objects.filter(full_name=name, birthday=birthday).first()
        if student_obj is None:
            birthday = datetime.datetime.strftime(birthday, "%Y-%m-%d")
            y, m, d = birthday.split('-')
            day_age = calculate_day_age(int(y), int(m), int(d))
            grade_obj = Grade.objects.filter(grade_name=grade).first()
            _class = StuClass.objects.get_or_create(school=school_obj, grade=grade_obj, name=_class)[0]
            student_obj = models.StudentInfo.objects.create(first_name=first_name, last_name=last_name,
                                                            school=school_obj,
                                                            grade=grade_obj,
                                                            full_name=name, birthday=birthday, gender=gender,
                                                            interior_student_id=uuid.uuid4(),
                                                            day_age=day_age, stu_class=_class
                                                            )
        return student_obj

    def __create_thread_pool(self):
        '''
        创建线程池
        :return:
        '''
        pool = ThreadPoolExecutor(4)

        return pool


class AssessmentCalculator(object):
    ''' 综合评估计算相关 '''

    def __init__(self):
        self.query = models.Answers.objects

    def get_assessment_list(self):
        '''
        获取所要计算的对象
        :return:
        '''
        return [item.id for item in models.QualityAssessmentSource.objects.all()]

    def cal(self):
        try:
            for obj in self.__get_obj():
                for name, fun in AssessmentCalculator.__dict__.items():
                    grade = models.QualityAssessmentSource.objects.filter(
                        id=obj).first().student.grade.get_grade_name_display()
                    if name.startswith("_cal"):
                        if hasattr(self, name):
                            fun(self, obj, grade=grade)
        except IndexError as e:

            print(e)

    def _cal_associate(self, obj, *args, **kwargs):
        '''
        计算联想
        :param obj:
        :return:
        '''
        grade = kwargs.get("grade")
        answer_list = ("B", "A", "B")
        if grade == "中班":
            answer_list = ("C", "A", "B")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="associate")
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(1, 2, final_score, obj)

    def _cal_cognition_of_number(self, obj, *args, **kwargs):
        '''
        计算数的认知
        :return:
        '''
        answer_list = ("A", "A")
        grade = kwargs.get("grade")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="cognition_of_number")
        if grade == "中班":
            answer_list = ("D", "A", "B", "D", "A")

        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(1, 3, final_score, obj)

    def _cal_logic(self, obj, *args, **kwargs):
        '''
        计算逻辑思维
        :param obj:
        :return:
        '''
        grade = kwargs.get("grade")
        answer_list = ("A", "B", "A", "A", "A", "C", "A", "A", "C", "C", "B", "E")
        if grade == "中班":
            answer_list = ("A", "B", "A", "A", "A", "C", "A", "A", "C", "C", "B", "E", "E", "D", "A", "C")

        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="logic")
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(1, 4, final_score, obj)

    def _cal_attention(self, obj, *args, **kwargs):
        '''
        计算注意力
        :param obj:
        :return:
        '''
        grade = kwargs.get("grade")
        base_number = 41
        score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="attention").count()
        if grade == "中班":
            base_number = 70
        final_score = self.__format_score(score / base_number * 100)
        self.__create_2_db(1, 5, final_score, obj)

    def _cal_short_memory(self, obj, *args, **kwargs):
        '''
        计算短时记忆
        :param obj:
        :return:
        '''
        grade = kwargs.get("grade")
        numbers = [2, 4, 5, 11, 15, 17, 18, 20]
        score = self.query.filter(boole_answer=True, assessment=obj, number__in=numbers,
                                  level_1_dimension="short_memory").count()
        if grade == "中班":
            numbers = [2, 4, 5, 6, 11, 14, 15, 17, 18, 20, 21, 24]
            score = self.query.filter(boole_answer=True, assessment=obj,
                                      number__in=numbers,
                                      level_1_dimension="short_memory").count()
        final_score = self.__format_score(score / len(numbers) * 100)
        self.__create_2_db(1, 6, final_score, obj)

    def _cal_science(self, obj, *args, **kwargs):
        '''
        计算科学常识
        :param obj:
        :return:
        '''
        grade = kwargs.get("grade")
        answer_list = ("A", "B", "A")
        if grade == "中班":
            answer_list = ("D", "B", "C")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="science")
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(1, 7, final_score, obj)

    def _cal_life(self, obj, *args, **kwargs):
        '''
        计算生活常识
        :param obj:
        :return:
        '''
        answer_list = ("A", "B")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="life")
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / 2 * 100)
        self.__create_2_db(1, 8, final_score, obj)

    def _cal_language_comprehension(self, obj, *args, **kwargs):
        '''
        计算语言理解
        :param obj:
        :return:
        '''
        # 中班小班题数相同答案不同
        grade = kwargs.get("grade")
        answer_list = ("C", "A", "B", "C", "A", "C", "A", "D", "D", "A", "C", "C", "A", "D", "C")
        if grade == "中班":
            answer_list = ("C", "A", "B", "D", "D", "C", "A", "D", "D", "C", "D", "D", "A", "B", "A")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="language_comprehension")
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(2, 9, final_score, obj)

    def _cal_language(self, obj, *args, **kwargs):
        '''
        计算语言表达
        :param obj:
        :return:
        '''
        condition = Q()
        q1 = Q()
        q1.children.append(("level_1_dimension", "language"))
        q2 = Q()
        q2.children.append(("level_2_dimension", 11))
        condition.add(q1, "OR")
        condition.add(q2, "OR")
        score = self.query.filter(condition, boole_answer=True, assessment=obj).count()
        final_score = self.__format_score(score / 43 * 100)
        self.__create_2_db(2, 10, final_score, obj)

    def _cal_colonial_existence(self, obj, *args, **kwargs):
        '''
        计算群体生活
        :return:
        '''
        obs_query = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="observe",
                                      level_2_dimension=9)
        grade = kwargs.get("grade")
        score = 0
        for answer_obj in obs_query:
            score += self.__parse_three_choice_one(answer_obj)
        society_query = self.query.filter(assessment=obj, level_2_dimension=18)
        society_answer = ("A", "A", "A")
        if grade == "中班":
            society_answer = ("C", "C", "A", "A", "B")
        society_score = self.__parse_choice_answer(society_query, society_answer)
        final_score = self.__format_score((score + society_score) / 6 * 100)
        self.__create_2_db(3, 11, final_score, obj)

    def _cal_rules_consciousness(self, obj, *args, **kwargs):
        '''
        计算规则意识
        :param obj:
        :return:
        '''
        obs_query = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="observe",
                                      level_2_dimension=7)
        score = 0
        base_num = 10
        grade = kwargs.get("grade")

        for answer_obj in obs_query:
            score += self.__parse_three_choice_one(answer_obj)
        society_query = self.query.filter(assessment=obj, level_1_dimension="society", level_2_dimension=19)
        society_answer = ("B", "A", "A", "A")
        if grade == "中班":
            society_answer = ("B", "A", "C", "B", "B")
            base_num = 11
        society_score = self.__parse_choice_answer(society_query, society_answer)
        final_score = self.__format_score((score + society_score) / base_num * 100)
        self.__create_2_db(3, 12, final_score, obj)

    def _cal_respect_for_others(self, obj, *args, **kwargs):
        '''
        计算尊重他人
        :param obj:
        :return:
        '''
        grade = kwargs.get("grade")
        answer_list = ("B", "A", "A")
        if grade == "中班":
            answer_list = ("D", "D", "D",)
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="society", level_2_dimension=21)
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / 3 * 100)
        self.__create_2_db(3, 13, final_score, obj)

    def _cal_autonomous_performance(self, obj, *args, **kwargs):
        '''计算自主表现'''
        answer_list = ("A", "B")
        grade = kwargs.get("grade")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="society", level_2_dimension=20)
        if grade == "中班":
            answer_list = ("C",)
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(3, 14, final_score, obj)

    def _cal_emotional_recognition(self, obj, *args, **kwargs):
        '''计算情绪识别'''
        obs_query = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="observe",
                                      level_2_dimension__in=[6, 7])
        score = 0
        for answer_obj in obs_query:
            score += self.__parse_three_choice_one(answer_obj)
        final_score = self.__format_score(score / 15 * 100)
        self.__create_2_db(3, 15, final_score, obj)

    def _cal_habits_of_life(self, obj, *args, **kwargs):
        '''计算生活习惯与卫生习惯'''
        grade = kwargs.get("grade")
        answer_list = ("A", "A", "A")
        if grade == "中班":
            answer_list = ("B", "A", "D")
        answer_data_query = self.query.filter(assessment=obj, level_1_dimension="habits_of_life")
        score = self.__parse_choice_answer(answer_data_query, answer_list)
        final_score = self.__format_score(score / len(answer_list) * 100)
        self.__create_2_db(4, 16, final_score, obj)

    def _cal_safety_consciousness(self, obj, *args, **kwargs):
        '''安全意识和自我保护'''

        obs_query = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="observe",
                                      level_2_dimension=5)
        grade = kwargs.get("grade")
        score = 0
        for answer_obj in obs_query:
            score += self.__parse_three_choice_one(answer_obj)

        safe_query = self.query.filter(assessment=obj, level_1_dimension="safety_consciousness", level_2_dimension=17)
        safe_answer = ("A",)
        if grade == "中班":
            safe_answer = ("b",)
        safe_score = self.__parse_choice_answer(safe_query, safe_answer)
        final_score = self.__format_score((score + safe_score) / 4 * 100)
        self.__create_2_db(4, 17, final_score, obj)

    def _cal_self_help_skills(self, obj, *args, **kwargs):
        '''计算自理能力'''

        obs_query = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="observe",
                                      level_2_dimension=10)
        grade = kwargs.get("grade")
        score = 0
        for answer_obj in obs_query:
            score += self.__parse_three_choice_one(answer_obj)

        safe_query = self.query.filter(assessment=obj, level_1_dimension="safety_consciousness", level_2_dimension=16)
        # 小班与中班的答案不同
        safe_answer = ("B", "B")
        if grade == "中班":
            safe_answer = ("B", "C")
        safe_score = self.__parse_choice_answer(safe_query, safe_answer)
        final_score = self.__format_score((score + safe_score) / 8 * 100)
        self.__create_2_db(4, 18, final_score, obj)

    def _cal_the_fine_arts(self, obj, *args, **kwargs):
        '''计算美术与书法'''
        arts_score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                       number__in=[1, 2, 3, 42, 43]).count()
        self.__create_2_db(6, 23, self.__format_score(arts_score), obj)

    def _cal_music(self, obj, *args, **kwargs):
        ''' 计算音乐'''
        music_score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                        number__in=[4, 5, 6, 28, 30, 32, 48]).count()
        self.__create_2_db(6, 24, self.__format_score(music_score), obj)

    def _cal_pm(self, obj, *args, **kwargs):
        '''计算体育'''
        PM_score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                     number__in=[7, 8, 9, 33, 34, 40, 45]).count()
        self.__create_2_db(6, 25, self.__format_score(PM_score), obj)

    def _cal_technology(self, obj, *args, **kwargs):
        '''计算高科技产品'''
        technology_score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                             number__in=[10, 11, 12, 31, 36]).count()
        self.__create_2_db(6, 26, self.__format_score(technology_score), obj)

    def _cal_logical_thinking(self, obj, *args, **kwargs):
        '''计算逻辑思维'''
        score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                  number__in=[13, 14, 15, 46, 47]).count()
        self.__create_2_db(6, 27, self.__format_score(score), obj)

    def _cal_scientific_investigation(self, obj, *args, **kwargs):
        '''计算科学探究'''
        score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                  number__in=[16, 17, 18, 41, 29, 37]).count()
        self.__create_2_db(6, 28, self.__format_score(score), obj)

    def _cal_society(self, obj, *args, **kwargs):
        '''计算社会'''
        score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                  number__in=[19, 20, 21, 25, 27, 38, 44, 39]).count()
        self.__create_2_db(6, 29, self.__format_score(score), obj)

    def _cal_law(self, obj, *args, **kwargs):
        '''计算法律与金融'''
        score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="interest",
                                  number__in=[22, 23, 26]).count()
        self.__create_2_db(6, 30, self.__format_score(score), obj)

    def _cal_power(self, obj, *args, **kwargs):
        '''计算力量'''
        score = 0
        power1 = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="sport",
                                   level_2_dimension=1, number__in=[1, 2, 3])
        power2 = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="sport",
                                   level_2_dimension=1, number__in=[4, 5, 6])
        if power1.exists():
            score += 1
        if power2.exists():
            score += 1

        final_score = score / 2 * 100
        self.__create_2_db(4, 31, self.__format_score(final_score), obj)

    def _cal_balance(self, obj, *args, **kwargs):
        '''计算平衡'''
        score = 0

        balance1 = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="sport",
                                     level_2_dimension=2, number__in=[7, 8, 9])
        balance2 = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="sport",
                                     level_2_dimension=2, number__in=[10, 11, 12])
        if balance1.exists():
            score += 1

        if balance2.exists():
            score += 1

        final_score = score / 2 * 100
        self.__create_2_db(4, 32, self.__format_score(final_score), obj)

    def _cal_speed(self, obj, *args, **kwargs):
        '''计算速度'''
        score = self.query.filter(assessment=obj, level_1_dimension="sport",
                                  level_2_dimension=3, float_score__lte=7.5).count()
        if score != 0:
            score = 100
        self.__create_2_db(4, 33, self.__format_score(score), obj)

    def _cal_hand_eye_coordination(self, obj, *args, **kwargs):
        '''计算手眼协调'''
        move_coin = self.query.filter(score_answer__isnull=False, assessment=obj, level_1_dimension="action",
                                      level_2_dimension=12, number__in=[1, 2])
        score = 0
        # 计算移动硬币
        for coin in move_coin:
            if coin.score_answer >= 4:
                score += 1
                break
        string = self.query.filter(score_answer__isnull=False, assessment=obj, level_1_dimension="action",
                                   level_2_dimension=12, number__in=[3, 4])

        for st in string:
            if st.score_answer >= 3:
                score += 1
                break

        final_score = score / 2 * 100
        self.__create_2_db(4, 34, self.__format_score(final_score), obj)

    def _cal_flexible_movement(self, obj, *args, **kwargs):
        '''计算动作灵活'''
        # 使用勺子
        user_spoon = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="action",
                                       number__in=[5, 6])
        score = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="action",
                                  level_2_dimension__in=[13]).exclude(number__in=[5, 6]).count()
        paint = self.query.filter(boole_answer=True, assessment=obj, level_1_dimension="action",
                                  level_2_dimension__in=[15]).count()
        if paint >= 3:
            score += 3
        else:
            score += paint
        if user_spoon.exists():
            score += 1
        final_score = score / 7 * 100
        self.__create_2_db(4, 35, self.__format_score(final_score), obj)

    def __create_2_db(self, top_dimension, level_2_dimension, score, obj):
        '''
        创建计算后的数据到数据库
        :param top_dimension:
        :param level_2_dimension:
        :param score:
        :param obj:
        :return:
        '''

        try:
            models.AssessmentScore.objects.update_or_create(top_dimension=top_dimension,
                                                            level_2_dimension=level_2_dimension,
                                                            assessment_id=obj,
                                                            defaults={"score": score})
        except Exception as e:
            print(e)

    def __get_obj(self):
        '''
        获取评测数据id
        :return:
        '''
        obj_list = self.get_assessment_list()
        for obj in obj_list:
            yield obj

    def __parse_three_choice_one(self, obj):
        '''
        解析三选一的分数
        :param obj:
        :return:
        '''
        number = obj.number
        if number % 3 == 1:
            return 3
        elif number % 3 == 2:
            return 2
        else:
            return 1

    def __parse_choice_answer(self, query, answer_list):
        '''
        解析选择题答案
        :param query:
        :param answer_list:
        :return:
        '''
        score = 0
        if len(query) == len(answer_list):
            pass
        else:
            if query.first():
                print("长度不等", query.first().get_level_2_dimension_display())
        for index, answer in enumerate(query):
            if index > len(answer_list) - 1:
                break
            if answer.get_choice_question_display() == answer_list[index]:
                score += 1
        return score

    def __format_score(self, score):
        score = format(score, '.2f')
        return score
