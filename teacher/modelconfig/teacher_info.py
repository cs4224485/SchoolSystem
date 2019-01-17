from stark.service.stark import StarkConfig, ChangeList
from django.urls import reverse, re_path
from django.shortcuts import HttpResponse, render
from django.conf import settings
from utils.common import *
from django.utils.safestring import mark_safe
from django import forms
from teacher import models
from django.forms import ValidationError
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets


class TeacherInfoConfig(StarkConfig):

    def display_name(self, row=None, header=False):
        if header:
            return "姓名"
        first_name, last_name, mark = shadow_name(row.first_name, row.last_name)
        html = '{0}<span style="font-size:21px; color:black; position: relative; top: 5px;">{1}</span>{2}'
        if mark:
            return mark_safe(html.format(last_name, mark, first_name))
        else:
            return mark_safe(html.format(last_name, '*', first_name))

    def get_add_btn(self):
        return None

    list_display = [display_name, 'school']
    search_list = ['full_name']
