import copy
from stark.service.stark import StarkConfig
from django.urls import reverse, re_path
from django.utils.safestring import mark_safe
from django import forms
from school import models
from django.forms import ValidationError
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from school.views import table_setting
from school.views import school_information


class SchoolInfoConfig(StarkConfig):

    def extra_urls(self):
        temp = []
        temp.append(re_path(r"class_manage/(?P<school_id>\d+)/$", school_information.ClassManage.as_view(),
                            name='school_info'))
        temp.append(re_path(r"school_calender/(?P<school_id>\d+)/$", school_information.SchoolCalender.as_view(),
                            name='school_calender'))
        temp.append(re_path(r"school_timetable/(?P<school_id>\d+)/$", school_information.SchoolTimeTable.as_view(),
                            name='school_timetables'))
        return temp

    def display_school_name(self, row=None, header=False):
        if header:
            return '学校名称'
        if row.campus_district:
            return "%s(%s)" % (row.school_name, row.campus_district)
        else:
            return "%s" % row.school_name

    def display_address(self, row=None, header=False):
        if header:
            return "校址"
        html = '''
            <div>
               <p>
                 <span>%s</span>
               </p>
               <p class='grey'>
                 <span>%s,</span> <span>%s,</span> <span>%s</span>
               </p>
            </div>
        ''' % (row.address, row.province, row.city, row.region)
        return mark_safe(html)

    def display_operation(self, row=None, header=False):
        if header:
            return '操作'

        edit_school_url = reverse('stark:school_schoolinfo_edit', args=(row.pk,))
        add_student_url = reverse('stark:students_studentinfo_add') + '?school_id=%s' % row.pk
        import_student_url = '/student/import_student/%s/' % row.pk
        class_manage_url = '/stark/school/schoolinfo/class_manage/%s/' % row.pk
        calender_url = '/stark/school/schoolinfo/school_calender/%s/' % row.pk
        cousre_tbale_url = '/stark/school/schoolinfo/school_timetable/%s/' % row.pk
        html = '''
            <div class='op_father'>
                <span><img src="/static/stark/imgs/op.png" width="18" height="18"></span>  
                <div class='op_list'>
                    <a href='%s'>编辑学校</a>
                    <a href='%s'>添加学生</a>
                    <a href='%s'>导入学生</a>
                    <a href='%s'>班级管理</a>
                    <a href='%s'>学校校历</a>
                    <a href='%s'>课程表</a>
                    <a>添加老师</a>
                </div>
            </div>
        ''' % (edit_school_url, add_student_url, import_student_url, class_manage_url, calender_url, cousre_tbale_url)
        return mark_safe(html)

    search_list = ['school_name']
    list_display = [display_school_name, 'school_type', 'school_layer', display_address, display_operation]

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)
        return val

    def get_model_form_class(self):
        '''
        创建添加学校相关信息的modelForm
        :return:
        '''

        class ModelForm(forms.ModelForm):
            class Meta:
                model = self.model_class
                fields = (
                    "school_name", "country", "province", 'city', 'region', "campus_district", "address",
                    "main_campus", "internal_id")

                widgets = {
                    "school_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
                    "province": Fwidgets.Select(
                        attrs={'class': 'form-control location', 'id': 'province', 'data-province': '---- 选择省 ----'}),
                    "city": Fwidgets.Select(
                        attrs={'class': 'form-control location', 'id': 'city', 'data-city': '---- 选择市 ----'}),
                    "region": Fwidgets.Select(
                        attrs={'class': 'form-control location', 'id': 'district', 'data-district': '---- 选择区县 ----'}),
                    "country": Fwidgets.Select(choices=((1, '中国'), (2, '日本'), (3, '美国'), (4, '韩国')),
                                               attrs={'class': 'form-control', 'style': 'width: 300px'}),
                    "main_campus": Fwidgets.RadioSelect(choices=((1, '本部'), (2, '分校或校区'))),
                    "address": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
                    "campus_district": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
                }

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
                # print(self.cleaned_data)
                # school_name = self.cleaned_data.get('school_name')
                campus = self.cleaned_data.get('campus_district')
                school_obj = models.SchoolInfo.objects.filter(**self.cleaned_data)
                if not school_obj:
                    return campus
                else:
                    raise ValidationError('该学校已存在')

        return ModelForm

    def get_edit_model_form_class(self):
        class ModelForm(forms.ModelForm):
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
                model = self.model_class
                fields = ("school_name", "English_name", "local_school_name", "country", "province", 'city', 'region',
                          "campus_district", "address",
                          'school_type', 'campus_english_name', 'website', 'school_layer', 'logo', 'pattern')

                widgets = {
                    "school_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
                    "abbreviation": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
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
                field_classes = {
                    'school_type': Ffields.ChoiceField
                }

                error_messages = {
                    "school_name": {"required": "请输入学校"},
                    "province": {"required": "请选择省市区"},
                    "address": {"required": "请输入学校地址"},
                }

        return ModelForm

    def get_add_form(self, model_form, request):
        import uuid
        # 随机的学校内部ID
        school_id = uuid.uuid4()
        request_data = copy.deepcopy(request.POST)
        request_data['internal_id'] = school_id
        form = model_form(request_data)
        return form

    def get_edit_form(self, model_form, request, obj):
        '''
        上传图片需要加request.FILES
        :param model_form:
        :param request:
        :return:
        '''
        form = model_form(request.POST, request.FILES, instance=obj)
        return form

    def add_view(self, request, template='stark/change.html'):
        return super().add_view(request, template='add_school.html')

    def change_view(self, request, pk, template='stark/change.html'):
        return super().change_view(request, pk, template='edit_school.html')


class ChoiceFieldConfig(StarkConfig):
    list_display = ['fieldName', 'field_english', 'field_type']


class SchoolSettingsConfig(StarkConfig):

    def get_add_btn(self):
        return mark_safe('<a href="%s" class="btn btn-success">添加</a>' % "/stark/school/tablesettings/settings/")

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)
        return val

    def extra_urls(self):
        temp = []
        temp.append(re_path(r"settings/$", table_setting.school_setting))
        temp.append(re_path(r"setting_edit/(\d+)/$", table_setting.edit_school_setting))
        temp.append(re_path(r"release/(\d+)/$", table_setting.release))
        temp.append(re_path(r"preview/$", table_setting.preview))
        return temp

    def display_release(self, row=None, header=None):
        if header:
            return '设置'
        url = '/stark/school/tablesettings/release/%s/' % row.pk
        tag = '<a href="%s">设置</a>' % url
        return mark_safe(tag)

    def display_edit(self, row=None, header=False):
        if header:
            return "编辑"
        url = '/stark/school/tablesettings/setting_edit/%s/' % row.pk
        return mark_safe(
            '<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a>' % url)

    def display_count(self, row=None, header=False):
        if header:
            return '填表人数'
        return row.table_info.all().count()

    list_display = ['title', 'stat_time', 'end_time', 'school_range', 'fill_range', display_count, display_release,
                    display_edit]


class SettingToFieldConfig(StarkConfig):
    list_display = ['setting', 'fields', 'order']
