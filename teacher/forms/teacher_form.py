from django import forms
from django.forms import ValidationError
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from school import models as scmodels
from teacher import models as teamodels
from django.forms import models as form_models


class TeacherEditModelForm(forms.ModelForm):
    birthday = Ffields.DateField(required=False, label='生日', widget=Fwidgets.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}))
    identity = form_models.ModelChoiceField(required=False, empty_label=None, label='身份',
                                            queryset=teamodels.Identity.objects.all(),
                                            widget=Fwidgets.RadioSelect())
    course = form_models.ModelMultipleChoiceField(required=False, label='所带课程', queryset=scmodels.Course.objects.all(),
                                                  widget=Fwidgets.CheckboxSelectMultiple())
    gender = Ffields.ChoiceField(required=False, label='性别', choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())

    class Meta:
        model = teamodels.TeacherInfo
        fields = ('last_name', 'first_name', 'gender', 'birthday', 'telephone', 'wechat', 'school', 'identity', 'course' )
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            'wechat': Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            'telephone': Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            'school': Fwidgets.Select(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        }
        error_messages = {
            "last_name": {"required": "请输入老师姓"},
            "first_name": {"required": "请输入老师名"},
            "gender": {"required": "请选择性别"},
        }
        labels = {
            'last_name': '老师姓(必填)',
            'first_name': '老师名(必填)',
        }
