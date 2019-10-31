#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/10/22'
from stark.service.stark import StarkConfig, Option
from django.shortcuts import render
from school.models import Course, QuestionBank


class QuestionBankConfig(StarkConfig):
    list_display = ['question_type', 'relate_course', 'crate_time', 'modify_time', 'crate_user']
    list_filter = [Option('question_type', is_choice=True, text_func=lambda x: x[1]),
                   Option('relate_course', is_choice=False)]

    def add_view(self, request, template='stark/change.html', *args, **kwargs):
        # 课程列表
        course_list = Course.objects.all()
        # 题型
        question_type = QuestionBank.question_type_choice

        return render(request, 'question_back/add_question.html', {'courses': course_list, 'type': question_type})
