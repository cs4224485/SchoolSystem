#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/7/30'

from rest_framework import serializers
from Django_apps.students.models import AssessmentScore, QualityAssessmentSource, Answers


class AssessmentSourceSerialize(serializers.ModelSerializer):
    grade = serializers.CharField(source='student.grade.get_grade_name_display')
    student = serializers.CharField(source='student.full_name')
    school = serializers.CharField(source='school.school_name')
    birthday = serializers.CharField(source='student.birthday')
    day_age = serializers.CharField(source='student.day_age')
    gender = serializers.CharField(source='student.get_gender_display')
    test_time = serializers.DateTimeField()

    class Meta:
        model = QualityAssessmentSource
        fields = ['id', 'student', 'school', "test_time", "grade", "birthday", "day_age", "gender"]
