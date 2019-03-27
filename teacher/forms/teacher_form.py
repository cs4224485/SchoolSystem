from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from school import models as scmodels
from teacher import models as teamodels
from django.forms import models as form_models
from stark.service.stark import StarkModelForm
from django.forms import ValidationError


class TeacherEditModelForm(StarkModelForm):
    birthday = Ffields.DateField(required=False, label='生日', widget=Fwidgets.DateInput(
        attrs={'type': 'date', 'style': 'width: 600px'}))
    identity = form_models.ModelChoiceField(required=False, empty_label=None, label='职务',
                                            queryset=teamodels.Identity.objects.all(),
                                            widget=Fwidgets.RadioSelect())
    course = form_models.ModelMultipleChoiceField(required=False, label='所带课程', queryset=scmodels.Course.objects.all(),
                                                  widget=Fwidgets.CheckboxSelectMultiple())
    gender = Ffields.ChoiceField(required=False, label='性别', choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())

    class Meta:
        model = teamodels.TeacherInfo
        fields = ('last_name', 'first_name', 'gender', 'birthday', 'telephone', 'wechat', 'school', 'identity', 'course' )
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'style': 'width: 600px'}),
            'wechat': Fwidgets.TextInput(attrs={'style': 'width: 600px'}),
            'telephone': Fwidgets.TextInput(attrs={'style': 'width: 600px'}),
            'school': Fwidgets.Select(attrs={'style': 'width: 600px'}),
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


class TeacherModelForm(StarkModelForm):
    birthday = Ffields.DateField(required=False, label='生日', widget=Fwidgets.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}))
    identity = form_models.ModelChoiceField(initial=1, empty_label=None, label='职务',
                                            queryset=teamodels.Identity.objects.all(),
                                            widget=Fwidgets.RadioSelect())
    course = form_models.ModelMultipleChoiceField(required=False, label='所带课程', queryset=scmodels.Course.objects.all(),
                                                  widget=Fwidgets.CheckboxSelectMultiple())
    gender = Ffields.ChoiceField(required=False, label='性别', choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())

    def __init__(self, *args, **kwargs):
        school_id = kwargs.pop('school_id')
        super(TeacherModelForm, self).__init__(*args, **kwargs)
        if school_id:
            self.school_id = school_id
            grade = form_models.ModelChoiceField(required=False,
                                                 queryset=scmodels.Grade.objects.
                                                 filter(stuclass__school_id=school_id).distinct(),
                                                 widget=Fwidgets.Select(
                                                     attrs={'class': 'form-control',
                                                            'id': 'grade'}), empty_label=None
                                                 )
            self.fields['grade'] = grade

    class Meta:
        model = teamodels.TeacherInfo
        fields = ('last_name', 'first_name', 'gender', 'birthday', 'telephone', 'wechat', 'identity', 'course')
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            'wechat': Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            'telephone': Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
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

    def clean(self):
        '''
        校验该教师是否已经存在
        :return:
        '''
        birthday = self.cleaned_data.get('birthday')
        last_name = self.cleaned_data.get('last_name')
        first_name = self.cleaned_data.get('first_name')
        teacher_obj = teamodels.TeacherInfo.objects.filter(birthday=birthday,
                                                           first_name=first_name,
                                                           last_name=last_name,
                                                           school=self.school_id)
        if teacher_obj:
            raise ValidationError('该教师已存在')
        return self.cleaned_data