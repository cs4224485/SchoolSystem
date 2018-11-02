from students import models
from django.shortcuts import render
from stark.service.stark import StarkConfig, Option
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from django import forms
from django.urls import re_path
from django.core import serializers
from django.http import JsonResponse
from utils.common import *
import copy


class StudentConfig(StarkConfig):

    def display_health(self, row=None, header=None):
        if header:
            return '健康信息'
        url = reverse('stark:students_healthinfo_self_changelist')
        tag = '<a href="%s?sid=%s">健康详情</a>' % (url, row.pk)
        return mark_safe(tag)

    def display_family(self, row=None, header=False):
        if header:
            return "家庭信息"
        url = reverse('stark:students_familyinfo_self_changelist')
        tag = '<a href="%s?sid=%s">家庭详情</a>' % (url, row.pk)
        return mark_safe(tag)

    def display_parent(self, row=None, header=False):
        if header:
            return "家长信息"
        url = reverse('stark:students_studenttoparents_self_changelist')
        tag = '<a href="%s?sid=%s">家长详情</a>' % (url, row.pk)
        return mark_safe(tag)

    def get_model_form_class(self):
        '''
        添加学生ModelForm验证
        :return:
        '''

        class ModelForm(forms.ModelForm):
            gender = Ffields.ChoiceField(required=True, choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())
            stu_class_list = tuple(models.StuClass.objects.filter(school=self.request.GET.get('school_id')))
            stu_class_list = [(item.pk, item) for item in stu_class_list]
            stu_class = Ffields.ChoiceField(required=True, choices=stu_class_list, widget=Fwidgets.Select(
                attrs={'class': 'form-control', 'id': 'class'}), error_messages={"required": "请选择班级"})
            grade_list = tuple(
                models.Grade.objects.filter(stuclass__school=self.request.GET.get('school_id')).all().distinct())
            grade_list = [(item.pk, item) for item in grade_list]
            grade_list.insert(0, (0, '--- 选择年级 ---'))
            grade = Ffields.ChoiceField(required=True, choices=grade_list, widget=Fwidgets.Select(
                attrs={'class': 'form-control', 'id': 'grade', 'data-province': '---- 选择年级 ----'}))

            class Meta:
                model = self.model_class
                fields = (
                "last_name", 'first_name', 'full_name', "gender", "birthday", 'school', 'period', 'interior_student_id')
                widgets = {
                    "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
                    "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
                    "birthday": Fwidgets.DateInput(
                        attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'})
                }
                error_messages = {
                    "last_name": {"required": "请输入学生姓"},
                    "first_name": {"required": "请输入学生名"},
                    "gender": {"required": "请选择性别"},
                }

        return ModelForm

    def add_view(self, request, template='stark/change.html'):
        return super().add_view(request, template='operation_table/add_student.html')

    def get_add_form(self, model_form, request):
        '''
        添加学生
        :param model_form:
        :param request:
        :return:
        '''
        request_data = copy.deepcopy(request.POST)
        school_id = request.GET.get('school_id')
        stu_class_obj = models.StuClass.objects.filter(id=request.POST.get('stu_class')).first()
        grade_obj = models.Grade.objects.filter(id=request.POST.get('grade')).first()
        request_data['school'] = school_id
        request_data['full_name'] = request_data['last_name'] + request_data['first_name']
        import uuid
        request_data['period'] = calculate_period(grade_obj.get_grade_name_display())
        request_data['interior_student_id'] = 'str:%s' % uuid.uuid4()
        form = model_form(request_data)

        form.instance.stu_class = stu_class_obj
        form.instance.grade = grade_obj
        return form

    def get_stu_class(self, request):
        '''
        根据年级过滤出学校的班级
        :param request:
        :return:
        '''

        school_id = request.GET.get('school_id')
        grade = request.GET.get('grade')
        # 筛选出符合父级要求的所有子级，因为输出的是一个集合，需要将数据序列化 serializers.serialize（）
        stu_class = serializers.serialize("json",
                                          models.StuClass.objects.filter(school=school_id, grade=grade).order_by(
                                              'name'))
        # 判断是否存在，输出
        if stu_class:
            return JsonResponse({'stu_class': stu_class})

    def extra_urls(self):
        temp = []
        temp.append(re_path("students/stu_class/", self.get_stu_class))
        return temp

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)
        return val

    def display_stu_class(self, row=None, header=False):
        if header:
            return '班级'
        return "%s(%s届)" % (row.stu_class, row.period)

    def get_add_btn(self):
        return None

    def display_name(self, row=None, header=False):
        if header:
            return "姓名"
        if len(row.first_name) > 1:
            first_name = row.first_name[-1]
            mark = '*'
            mark *= len(row.first_name) - 1
            return mark_safe('%s<span style="font-size:21px; color:black; position: relative; top: 5px;">%s</span>%s' % (row.last_name, mark, first_name))
        return mark_safe('%s<span style="font-size:21px; color:black; position: relative; top: 5px;">*</span>%s' % (row.last_name, row.first_name))

    list_display = [display_name, display_stu_class, 'school']
    search_list = ['full_name']


class SelfHealthInfoConfig(StarkConfig):
    '''
    学生个人健康信息配置
    '''

    def get_queryset(self):
        sid = self.request.GET.get('sid')
        return models.HealthInfo.objects.filter(student=sid)

    def get_list_display(self):
        val = ['student', 'height', 'weight', 'vision_left', 'vision_right', 'blood_type', 'record_date']
        return val


class SelfFamilyInfoConfig(StarkConfig):
    '''
    学生个人家庭信息配置
    '''

    def get_queryset(self):
        sid = self.request.GET.get('sid')
        return models.FamilyInfo.objects.filter(student=sid)

    list_display = ['student', 'family_status', 'living_type', 'language', ]


class SelfParentsInfoConfig(StarkConfig):
    '''
    学生个人家长信息
    '''

    def get_queryset(self):
        sid = self.request.GET.get('sid')
        return models.StudentToParents.objects.filter(student=sid).all()

    list_display = ['student', 'parents', 'relation']
