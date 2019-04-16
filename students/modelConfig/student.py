import copy
from students import models
from stark.service.stark import StarkConfig, Option
from django.utils.safestring import mark_safe
from students.forms.student_form import StudentEditForm
from django.urls import re_path
from utils.common import *


class StudentConfig(StarkConfig):

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        return StudentEditForm

    def get_form(self, model_form, request, modify=False, *args, **kwargs):
        if modify:
            obj = kwargs.get('obj')
            request_data = copy.deepcopy(request.POST)
            stu_class_obj = models.StuClass.objects.filter(id=request.POST.get('stu_class')).first()
            grade_obj = models.Grade.objects.filter(id=request.POST.get('grade')).first()
            birthday = request_data.get('birthday')
            # 如果提交了生日信息需要算出星座日龄年龄等信息
            if birthday:
                result = calculate_info(birthday)
                if result:
                    request_data['constellation'] = result.get('constellations')
                    request_data['chinese_zodiac'] = result.get('ChineseZodiac')
                    request_data['age'] = result.get('age')
                    request_data['day_age'] = result.get('day_age')
            if grade_obj:
                request_data['period'] = calculate_period(grade_obj.get_grade_name_display())
            request_data['full_name'] = request_data['last_name'] + request_data['first_name']
            form = model_form(request_data, instance=obj)
            form.instance.stu_class = stu_class_obj
            form.instance.grade = grade_obj
            return form

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        return super(StudentConfig, self).change_view(request, pk, template='tables/edit_student.html', *args, **kwargs)

    def get_urls(self):
        urlpatterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^(?P<pk>\d+)/change/', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path(r'^(?P<pk>\d+)/del/', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())
        return urlpatterns

    def get_list_display(self):
        val = super().get_list_display()
        return val

    def display_stu_class(self, row=None, header=False, *args, **kwargs):
        if header:
            return '班级'
        return "%s(%s届)" % (row.stu_class, row.period)

    def get_add_btn(self):
        return None

    def display_name(self, row=None, header=False, *args, **kwargs):
        if header:
            return "姓名"
        first_name, last_name, mark = shadow_name(row.first_name, row.last_name)
        html = '{0}<span style="font-size:21px; color:black; position: relative; top: 5px;">{1}</span>{2}'
        if mark:
            return mark_safe(html.format(last_name, mark, first_name))
        else:
            return mark_safe(html.format(last_name, '*', first_name))

    list_display = [display_name, display_stu_class, 'school']
    search_list = ['full_name']


