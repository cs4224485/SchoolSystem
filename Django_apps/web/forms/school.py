from django import forms
from django.forms import ValidationError
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from school import models as scmodels


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



