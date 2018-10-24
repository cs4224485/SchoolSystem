from students import models
from stark.service.stark import StarkConfig, Option
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from django import forms
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
            stu_class_list = tuple(models.StuClass.objects.filter(school=self.request.GET.get('school_id')).distinct())
            stu_class_list = [(item.pk, item) for item in stu_class_list]
            stu_class = Ffields.ChoiceField(required=True, choices=stu_class_list, widget=Fwidgets.Select(
                attrs={'class': 'form-control', 'style': 'width: 600px'}), error_messages={"required": "请选择班级"})

            class Meta:
                model = self.model_class
                fields = ("last_name", 'first_name', 'full_name', "gender", "birthday", 'school', 'interior_student_id')
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
        request_data = copy.deepcopy(request.POST)
        stu_class_obj = models.StuClass.objects.filter(id=request.POST.get('stu_class')).first()
        grade_obj = stu_class_obj.grade
        school_id = request.GET.get('school_id')
        request_data['school'] = school_id
        request_data['full_name'] = request_data['last_name']+request_data['first_name']
        import uuid
        request_data['interior_student_id'] = 'str:%s' % uuid.uuid4()
        form = model_form(request_data)
        form.instance.stu_class = stu_class_obj
        form.instance.grade = grade_obj
        return form

    list_display = ['full_name', display_health, display_family,  display_parent, 'id_card']
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
