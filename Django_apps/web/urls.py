#!/usr/bin/env python
# -*- coding: utf-8 -*-
__title__ = ''
__author__ = '君集003'
__mtime__ = '2019/7/15'

from django.urls import path, include, re_path
from web.views import assessment

urlpatterns = [
    re_path("ass_upload/$", assessment.upload_source_data, name="assUpload"),
    re_path("ass_download/$", assessment.export_cal_data, name="assDownload")
]