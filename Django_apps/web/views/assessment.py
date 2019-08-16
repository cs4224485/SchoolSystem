#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = '综合素质评估'
__author__ = '君集003'
__mtime__ = '2019/7/15'

from django.shortcuts import render, HttpResponse
from web.service.assessment_handler import AssessmentHandler
from Django_apps.students.models import QualityAssessmentSource, AssessmentScore
from utils.file_handler import ExcelFileHandler


def upload_source_data(request):
    '''上传综合素质评估原始数据'''

    if request.method == "GET":
        return render(request, "tables/student_import.html")

    context = {'status': True, 'msg': '导入成功'}
    try:
        as_obj = AssessmentHandler(request)
        as_obj.import_source_data()
    except Exception as e:
        print(e)
        context['status'] = False
        context['msg'] = '导入失败'
    return render(request, 'tables/student_import.html', context)


def export_cal_data(request):
    '''
    导出计算后的数据
    :param request:
    :return:
    '''

    if request.method == "GET":
        return render(request, "data_download.html")

    filed_head = ['ID', '姓名', '班级', '年级']
    ignore_fields = [i for i in range(20, 31)]
    ignore_fields.extend([1, 19])
    for field in AssessmentScore.level_2_dimension_choice:
        if field[0] in ignore_fields:
            continue
        filed_head.append(field[1])

    data_list = []
    for assessment_obj in QualityAssessmentSource.objects.select_related():
        id = assessment_obj.id
        name = assessment_obj.student.full_name
        _class = assessment_obj.student.stu_class.name
        grade = assessment_obj.student.grade.get_grade_name_display()
        row_data_list = [id, name, _class, grade]
        # 将ID, 姓名,班级,年级过滤出去
        filter_list = filter(lambda x: filed_head.index(x) > 3, filed_head)
        for fields in list(filter_list):
            score_obj = None
            db_number = get_fields_number(fields, AssessmentScore.level_2_dimension_choice)
            if db_number:
                score_obj = AssessmentScore.objects.filter(level_2_dimension=db_number, assessment=assessment_obj).first()
            if score_obj:
                row_data_list.append(score_obj.score)
            else:
                row_data_list.append("")
        data_list.append(row_data_list)

    # 创建Excel
    excel_obj = ExcelFileHandler(filed_head)
    response, file_path = excel_obj.down_load_file(data_list)
    excel_obj.remove_file(file_path)
    return response


def get_fields_number(field, db_list):
    '''获取字段在数据库中编号'''
    try:
        for item in db_list:
            if field == item[1]:
                return item[0]
    except Exception as e:
        return None
