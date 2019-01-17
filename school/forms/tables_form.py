from django import forms
from django.forms import ValidationError
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from students import models as stumodels
from school import models as scmodels
from teacher import models as teamodels
from django.forms import models as form_models


class SchoolBaseForm(forms.ModelForm):
    base_weight = {
        "school_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        "province": Fwidgets.Select(
            attrs={'class': 'form-control location', 'id': 'province', 'data-province': '---- 选择省 ----'}),
        "city": Fwidgets.Select(
            attrs={'class': 'form-control location', 'id': 'city', 'data-city': '---- 选择市 ----'}),
        "region": Fwidgets.Select(
            attrs={'class': 'form-control location', 'id': 'district', 'data-district': '---- 选择区县 ----'}),
        "country": Fwidgets.Select(choices=((1, '中国'), (2, '日本'), (3, '美国'), (4, '韩国')),
                                   attrs={'class': 'form-control', 'style': 'width: 300px'}),
        "address": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        "campus_district": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
    }


class SchoolAddForm(SchoolBaseForm):
    class Meta:
        model = scmodels.SchoolInfo
        fields = (
            "school_name", "country", "province", 'city', 'region', "campus_district", "address",
            "main_campus", "internal_id")

        widgets = {
            "main_campus": Fwidgets.RadioSelect(choices=((1, '本部'), (2, '分校或校区'))),
        }
        widgets.update(SchoolBaseForm.base_weight)
        error_messages = {
            "school_name": {"required": "请输入学校"},
            "province": {"required": "请选择省市区"},
            "address": {"required": "请输入学校地址"},
        }

    def clean_campus_district(self):
        '''
        判断学校是否已经存在了
        :return:
        '''
        school_name = self.cleaned_data.get('school_name')
        campus = self.cleaned_data.get('campus_district')
        school_obj = scmodels.SchoolInfo.objects.filter(school_name=school_name, campus_district=campus)
        if not school_obj:
            return campus
        else:
            raise ValidationError('该学校已存在')


class SchoolEditModelForm(SchoolBaseForm):
    English_name = Ffields.CharField(required=False, widget=Fwidgets.TextInput(
        attrs={'class': 'form-control', 'style': 'width: 600px'}))
    local_school_name = Ffields.CharField(required=False, widget=Fwidgets.TextInput(
        attrs={'class': 'form-control', 'style': 'width: 600px'}))
    campus_english_name = Ffields.CharField(required=False, widget=Fwidgets.TextInput(
        attrs={'class': 'form-control', 'style': 'width: 600px'}))
    website = Ffields.URLField(required=False, widget=Fwidgets.TextInput(
        attrs={'class': 'form-control', 'style': 'width: 600px'}))
    school_type = Ffields.ChoiceField(required=False, choices=((1, '公立'), (2, '民办')),
                                      widget=Fwidgets.RadioSelect())
    school_layer = Ffields.ChoiceField(required=False, choices=(
        (1, '幼儿园'), (2, '小学'), (3, '初中'), (4, '高中阶段'), (5, '九年一惯制'), (6, '中等职业学校'), (7, '十二年一贯制')),
                                       widget=Fwidgets.RadioSelect(attrs={'class': 'school_layer'}))
    logo = Ffields.FileField(required=False, widget=Fwidgets.FileInput(attrs={'style': 'display:none'}))
    pattern = Ffields.FileField(required=False, widget=Fwidgets.FileInput(attrs={'style': 'display:none'}))

    class Meta:
        model = scmodels.SchoolInfo
        fields = ("school_name", "English_name", "local_school_name", "country", "province", 'city', 'region',
                  "campus_district", "address",
                  'school_type', 'campus_english_name', 'website', 'school_layer', 'logo', 'pattern')

        widgets = {
            "abbreviation": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
        }
        widgets.update(SchoolBaseForm.base_weight)

        error_messages = {
            "school_name": {"required": "请输入学校"},
            "province": {"required": "请选择省市区"},
            "address": {"required": "请输入学校地址"},
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
            attrs={'class': 'form-control', 'id': 'grade', 'data-province': '---- 选择年级 ----'}))
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


class TeacherModelForm(forms.ModelForm):
    birthday = Ffields.DateField(required=False, label='生日', widget=Fwidgets.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}))
    identity = form_models.ModelChoiceField(required=False, empty_label=None, label='身份',
                                            queryset=teamodels.Identity.objects.all(),
                                            widget=Fwidgets.RadioSelect())
    course = form_models.ModelMultipleChoiceField(required=False, label='所带课程', queryset=scmodels.Course.objects.all(),
                                                  widget=Fwidgets.CheckboxSelectMultiple())
    gender = Ffields.ChoiceField(required=False, choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())

    def __init__(self, *args, **kwargs):
        school_id = kwargs.pop('school_id')
        super(TeacherModelForm, self).__init__(*args, **kwargs)
        if school_id:
            grade = form_models.ModelChoiceField(required=False,
                                                 queryset=scmodels.Grade.objects.
                                                 filter(stuclass__school_id=school_id).distinct(),
                                                 widget=Fwidgets.Select(
                                                     attrs={'class': 'form-control',
                                                            'id': 'grade'})
                                                 )
            self.fields['grade'] = grade

    class Meta:
        model = teamodels.TeacherInfo
        fields = ('last_name', 'first_name', 'gender', 'birthday', 'wechat', 'identity', 'course')
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            'wechat': Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            # "gender": Fwidgets.RadioSelect()
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


class GenderField(Ffields.ChoiceField):

    def __init__(self):
        super(GenderField, self).__init__()