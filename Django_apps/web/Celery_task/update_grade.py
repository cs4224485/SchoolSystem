#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/9/29'

from Django_apps.students.models import StudentInfo, GraduatedStudent
from school.models import StuClass, Grade
from SchoolInfomationSystem.celery import celery_task
import time


@celery_task.task
def upgrade_student_grade():
    student_queryset = StudentInfo.objects.exclude(school_id__in=[292, 291, 69], graduate_student__isnull=True)
    for item in student_queryset:
        grade = item.grade.grade_name
        class_name = item.stu_class.name if item.stu_class else None
        school = item.school
        # 暂时设置为如果年级是6年级把该学生设置为毕业生
        if grade == 6:
            GraduatedStudent.objects.update_or_create(from_school=school, graduate=item)
            item.stu_class = None
        else:
            new_class = StuClass.objects.filter(grade__grade_name=grade+1, name=class_name, school=school).first()
            item.stu_class = new_class
        item.grade = Grade.objects.filter(grade_name=grade + 1).first()
        item.save()

