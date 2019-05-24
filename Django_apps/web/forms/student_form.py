from django import forms
from django.forms import ValidationError
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from Django_apps.students import models as stumodels
from stark.forms.widgets import DateTimePickerInput


class StudentEditForm(forms.ModelForm):
    gender = Ffields.ChoiceField(required=True, choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())
    birthday = Ffields.DateField(required=False, widget=DateTimePickerInput(
        attrs={ 'type': 'date', 'style': 'width: 600px'}))

    class Meta:
        model = stumodels.StudentInfo
        fields = ("last_name", 'first_name', 'full_name', "gender", "birthday", 'period', 'school', 'period',
                  'age', 'day_age', 'constellation', 'chinese_zodiac', 'school')
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "school": Ffields.Select(attrs={'class': 'form-control', 'style': 'width: 600px'})
        }


class StudentModelForm(forms.ModelForm):
    gender = Ffields.ChoiceField(required=False, choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())
    birthday = Ffields.DateField(required=False, widget=Fwidgets.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}))

    def __init__(self, *args, **kwargs):
        school_id = kwargs.pop('school_id')
        super(StudentModelForm, self).__init__(*args, **kwargs)
        stu_class_list = tuple(stumodels.StuClass.objects.filter(school_id=school_id))
        stu_class_list = [(item.pk, item) for item in stu_class_list]
        stu_class = Ffields.ChoiceField(required=True, choices=stu_class_list, widget=Fwidgets.Select(
            attrs={'class': 'form-control', 'id': 'class'}), error_messages={"required": "请选择班级"})
        grade_list = tuple(stumodels.Grade.objects.filter(stuclass__school_id=school_id).all().distinct())
        grade_list = [(item.pk, item) for item in grade_list]
        grade_list.insert(0, (0, '--- 选择年级 ---'))
        grade = Ffields.ChoiceField(required=True, choices=grade_list, widget=Fwidgets.Select(
            attrs={'class': 'form-control', 'id': 'grade'}))
        self.fields['grade'] = grade
        self.fields['stu_class'] = stu_class

    class Meta:
        model = stumodels.StudentInfo
        fields = (
            "last_name", 'first_name', 'full_name', "gender", "birthday", 'school', 'period',
            'interior_student_id', 'age', 'day_age', 'constellation', 'chinese_zodiac')
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        }
        error_messages = {
            "last_name": {"required": "请输入学生姓"},
            "first_name": {"required": "请输入学生名"},
            "gender": {"required": "请选择性别"},
        }

    def clean(self):
        '''
        校验该学生是否已经存在
        :return:
        '''
        birthday = self.cleaned_data.get('birthday')
        last_name = self.cleaned_data.get('last_name')
        first_name = self.cleaned_data.get('first_name')
        student_obj = stumodels.StudentInfo.objects.filter(first_name=first_name,
                                                           last_name=last_name, birthday=birthday)
        if student_obj:
            raise ValidationError('该学生已存在')
        return self.cleaned_data
