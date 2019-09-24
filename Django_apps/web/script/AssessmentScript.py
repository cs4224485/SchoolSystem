#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/7/22'
import os
import sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolInfomationSystem.settings_dev')
base_dir = '/'.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))).split("/")[:-1])
sys.path.append(base_dir)
import django

django.setup()

from web.service.assessment_handler import AssessmentCalculator

if __name__ == '__main__':
    cal_obj = AssessmentCalculator()
    cal_obj.cal()
