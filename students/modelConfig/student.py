import copy
from students import models
from stark.service.stark import StarkConfig, Option
from django.urls import reverse
from django.utils.safestring import mark_safe
from students.forms.student_form import StudentEditForm
from django.urls import re_path
from django.core import serializers
from django.http import JsonResponse
from utils.common import *


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

    def get_edit_model_form_class(self):
        return StudentEditForm

    def get_edit_form(self, model_form, request, obj):
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

    def change_view(self, request, pk, template='stark/change.html'):
        return super(StudentConfig, self).change_view(request, pk, template='tables/edit_student.html')

    def get_urls(self):
        urlpatterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^(?P<pk>\d+)/change/', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path(r'^(?P<pk>\d+)/del/', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())
        return urlpatterns

    def get_stu_class(self, request):
        '''
        根据年级过滤出学校的班级
        :param request:
        :return:
        '''
        school_id = request.GET.get('school_id')
        grade = request.GET.get('grade', 7)
        # 筛选出符合父级要求的所有子级，因为输出的是一个集合，需要将数据序列化 serializers.serialize（）
        class_queryset = order_by_class(
            list(models.StuClass.objects.filter(school=school_id, grade=grade).order_by('name')))
        grade_queryset = models.Grade.objects.filter(stuclass__school_id=school_id).distinct()
        grade_list = []
        for item in grade_queryset:
            grade_list.append({'id': item.id, 'grade': item.get_grade_name_display()})
        stu_class = serializers.serialize("json", class_queryset)
        # 判断是否存在，输出
        if stu_class:
            return JsonResponse({'stu_class': stu_class, 'grade_list': grade_list, 'code': 200})
        else:
            return JsonResponse({'stu_class': []})

    def extra_urls(self):
        temp = []
        temp.append(re_path("filter_class/", self.get_stu_class))
        return temp

    def get_list_display(self):
        val = super().get_list_display()
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
        first_name, last_name, mark = shadow_name(row.first_name, row.last_name)
        html = '{0}<span style="font-size:21px; color:black; position: relative; top: 5px;">{1}</span>{2}'
        if mark:
            return mark_safe(html.format(last_name, mark, first_name))
        else:
            return mark_safe(html.format(last_name, '*', first_name))

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
