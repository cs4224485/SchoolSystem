#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/7/30'

import decimal
from rest_framework.views import APIView, Response
from Django_apps.students.models import AssessmentScore, QualityAssessmentSource, Answers
from APIS.serialize.assessment import AssessmentSourceSerialize
from utils.base_response import BaseResponse
from django.utils.decorators import method_decorator


def get_assessment_obj(func):
    '''
    获取评测信息对象装饰器
    :param func:
    :return:
    '''

    def inner(request, *args, **kwargs):
        assessment_id = kwargs.get("pk")
        res = BaseResponse()
        ass_query = QualityAssessmentSource.objects.filter(id=assessment_id).first()
        if not ass_query:
            res.msg = "未找到该数据"
            res.code = 404
            return Response(res.get_dict)

        return func(request, ass_obj=ass_query, *args, **kwargs)

    return inner


def get_score(ass_obj, top_dimension):
    '''获取每个维度的分数'''
    query = AssessmentScore.objects
    score_query = query.filter(assessment=ass_obj, top_dimension=top_dimension).select_related()
    data_dict = {}
    for obj in score_query:
        data_dict[obj.get_level_2_dimension_display()] = obj.score

    return data_dict


def get_total_score(data_dict):
    '''
    计算总分
    :param data_dict:
    :return:
    '''
    score = 0
    for key, value in data_dict.items():
        score += value
    decimal.getcontext().prec = 4
    return score / len(data_dict)


class BaseInfoViewSet(APIView):
    '''获取基础信息'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        ass_query = kwargs.get("ass_obj")
        try:
            ass_se = AssessmentSourceSerialize(ass_query)
            res.data = ass_se.data
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = "服务器端错误"
        return Response(res.get_dict)


class HealthViewSet(APIView):
    '''健康维度相关信息'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        ass_query = kwargs.get("ass_obj")
        res = BaseResponse()
        data_dict = get_score(ass_query, 4)
        decimal.getcontext().prec = 4
        data_dict['大运动'] = (data_dict['力量'] + data_dict['平衡'] + data_dict['速度']) / 3
        data_dict['精细动作'] = (data_dict['手眼协调'] + data_dict['动作灵活']) / 2
        data_dict['健康总分'] = (decimal.Decimal(data_dict['大运动'])
                             + data_dict['生活习惯与卫生习惯']
                             + data_dict['安全意识和自我保护']
                             + data_dict['自理能力']
                             + decimal.Decimal((data_dict['精细动作']))) / 5

        res.data = data_dict
        res.code = 200
        return Response(res.get_dict)


class LanguageViewSet(APIView):
    '''语言理解'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        ass_query = kwargs.get("ass_obj")
        res = BaseResponse()
        try:
            data_dict = get_score(ass_query, 2)
            total_score = get_total_score(data_dict)
            data_dict['语言总分'] = total_score
            res.data = data_dict
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = "服务器端错误"
        return Response(res.get_dict)


class ScienceViewSet(APIView):
    '''科学'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        ass_query = kwargs.get("ass_obj")
        res = BaseResponse()
        try:
            data_dict = get_score(ass_query, 1)
            total_score = get_total_score(data_dict)
            data_dict['科学总分'] = total_score
            res.data = data_dict
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = "服务器端错误"
        return Response(res.get_dict)


class SocietyViewSet(APIView):
    '''社会'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        ass_query = kwargs.get("ass_obj")
        res = BaseResponse()
        try:
            data_dict = get_score(ass_query, 3)
            total_score = get_total_score(data_dict)
            data_dict['社会总分'] = total_score
            res.data = data_dict
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = "服务器端错误"
        return Response(res.get_dict)


class InterestViewSet(APIView):
    '''兴趣爱好'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        ass_query = kwargs.get("ass_obj")
        res = BaseResponse()
        try:
            data_dict = get_score(ass_query, 6)
            interest_query = Answers.objects.filter(level_1_dimension="interest", number__gte=25,
                                                    assessment=ass_query).select_related()
            for obj in interest_query:
                data_dict[obj.excel_col_des] = obj.boole_answer
            res.code = 200
            res.data = data_dict
        except Exception as e:
            res.code = 500
            res.msg = "服务器端错误"
        return Response(res.get_dict)


class ArtViewSet(APIView):
    '''艺术'''

    @method_decorator(get_assessment_obj)
    def get(self, request, *args, **kwargs):
        ass_query = kwargs.get("ass_obj")
        res = BaseResponse()
        try:
            art_query = Answers.objects.filter(level_1_dimension="art", assessment=ass_query)
            data_dict = {}
            for obj in art_query:
                data_dict[obj.excel_col_des] = obj.get_choice_question_display()
            # 画小花
            draw = Answers.objects.filter(level_1_dimension="action", assessment=ass_query, number__gte=13,
                                          boole_answer=True).count()
            data_dict['画小花'] = draw
            res.code = 200
            res.data = data_dict
        except Exception as e:
            res.code = 500
            res.msg = "服务器端错误"
        return Response(res.get_dict)
