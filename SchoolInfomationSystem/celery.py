#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/9/29'

from celery import Celery
import os
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SchoolInfomationSystem.settings_dev')  # 设置django环境
celery_task = Celery("task")
celery_task.config_from_object('django.conf:settings', namespace='CELERY')
celery_task.conf.beat_schedule = {
    "each10s_task": {
        "task": "Django_apps.web.Celery_task.update_grade.upgrade_student_grade",
        "schedule": crontab(minute="*/10"),  # 每5分钟钟执行一次
    },
}
