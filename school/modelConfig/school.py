import copy
from stark.service.stark import StarkConfig, ChangeList
from django.urls import reverse, re_path
from django.shortcuts import HttpResponse, render, redirect
from django.conf import settings
from django.utils.safestring import mark_safe
from school import models
from school.views import table_setting
from school.views import school_information
from school.forms.tables_form import StudentModelForm, SchoolAddForm, SchoolEditModelForm, TeacherModelForm
from teacher import models as tea_models
from utils.common import *


class SchoolInfoConfig(StarkConfig):

    def list_view(self, request):
        '''
        查看学校的列表页面
        :param request:
        :return:
        '''

        if request.method == 'POST':
            action_name = request.POST.get('actions')
            action_dict = self.get_action_dict()
            if action_name not in action_dict:
                return HttpResponse('非法请求')

            response = getattr(self, action_name)(request)
            if response:
                return response

        # 处理搜索
        search_list, keyword, con = self.search_condition(request)

        # ##### 处理分页 #####
        from stark.utils.page import Pagination
        # 全部数据
        total_set = self.model_class.objects.filter(con).count()

        # 携带参数
        query_params = request.GET.copy()
        query_params._mutable = True
        # 请求的URL
        base_url = self.request.path
        page = Pagination(total_set, request.GET.get('page'), query_params, base_url, per_page=20)
        # 获取组合搜索筛选
        list_filter = self.get_list_filter()

        try:
            # 搜索条件无法匹配到数据时可能会出现异常
            origin_queryset = self.get_queryset()
            queryset = origin_queryset.filter(con).filter(**self.get_list_filter_condition(request)).order_by(
                *self.get_order_by()).distinct()[page.start:page.end]
        except Exception as e:
            queryset = []
        cl = ChangeList(self, queryset, keyword, search_list, page.page_html())

        context = {
            'cl': cl,
        }
        return render(request, 'stark/changelist.html', context)

    def extra_urls(self):
        temp = []
        temp.append(re_path(r"class_manage/(?P<school_id>\d+)/$",
                            self.wrapper(school_information.ClassManage.as_view()),
                            name='class_manage'))
        temp.append(re_path(r"school_calender/(?P<school_id>\d+)/$",
                            self.wrapper(school_information.SchoolCalender.as_view()),
                            name='school_calender'))
        temp.append(re_path(r"school_timetable/(?P<school_id>\d+)/$",
                            self.wrapper(school_information.SchoolTimeTable.as_view()),
                            name='school_timetables'))
        temp.append(re_path(r"add_student/(?P<school_id>\d+)/$", self.wrapper(self.add_student), name='add_student'))
        temp.append(re_path(r"add_teacher/(?P<school_id>\d+)/$", self.wrapper(self.add_teacher), name='add_teacher'))
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
        edit_school_url = self.reverse_edit_url(row.pk)
        add_student_url = self.reverse_commons_url('add_student', row.pk)
        add_teacher_url = self.reverse_commons_url('add_teacher', row.pk)
        import_student_url = '/student/import_student/%s/' % row.pk
        class_manage_url = self.reverse_commons_url('class_manage', row.pk)
        calender_url = self.reverse_commons_url('school_calender', row.pk)
        course_tbale_url = self.reverse_commons_url('school_timetables', row.pk)
        html = '''
            <div class='op_father'>
                <span><image src="/static/stark/imgs/op.png" width="18" height="18"></span>  
                <div class='op_list'>
                    <a href='%s'>编辑学校</a>
                    <a href='%s'>添加学生</a>
                    <a href='%s'>导入学生</a>
                    <a href='%s'>添加老师</a>
                    <a href='%s'>班级管理</a>
                    <a href='%s'>学校校历</a>
                    <a href='%s'>课程表</a>
                </div>
            </div>
        ''' % (edit_school_url, add_student_url, import_student_url,
               add_teacher_url, class_manage_url, calender_url, course_tbale_url)
        return mark_safe(html)

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)
        return val

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        '''
        创建添加学校相关信息的modelForm
        :return:
        '''
        if is_add:
            return SchoolAddForm
        return SchoolEditModelForm

    def get_form(self, model_form, request, modify=False, *args, **kwargs):
        if not modify:
            import uuid
            # 随机的学校内部ID
            school_id = uuid.uuid4()
            request_data = copy.deepcopy(request.POST)
            request_data['internal_id'] = school_id
            form = model_form(request_data)
            return form
        obj = kwargs.get('obj')
        school_layer = int(request.POST.get('school_layer', 0))
        school_id = obj.id
        form = model_form(request.POST, request.FILES, instance=obj)
        # 根据学校得层级创建年级,每个年级默认创建一班
        if school_layer > 0 and school_layer != obj.school_layer:
            models.StuClass.objects.exclude(grade__grade_name__in=settings.SCHOOL_GRADE_MAPPING[school_layer]).filter(
                school_id=school_id).delete()
            create_list = []
            for i in settings.SCHOOL_GRADE_MAPPING[school_layer]:
                query = models.StuClass.objects.filter(school_id=school_id, grade__grade_name=i)
                if query:
                    continue
                grade_obj = models.Grade.objects.filter(grade_name=i).first()
                obj = models.StuClass(school_id=school_id, grade=grade_obj, name='1班')
                create_list.append(obj)
            models.StuClass.objects.bulk_create(create_list)
        return form

    def add_student(self, request, school_id):
        '''
          添加学生
          :param model_form:
          :param request:
          :param school_id:学校ID
          :return:
          '''

        if request.method == 'GET':
            form = StudentModelForm(school_id=school_id)
            return render(request, 'tables/add_student.html', {'form': form, 'school_id': school_id})
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
        request_data['school'] = school_id
        request_data['full_name'] = request_data['last_name'] + request_data['first_name']
        import uuid
        if grade_obj:
            request_data['period'] = calculate_period(grade_obj.get_grade_name_display())
        request_data['interior_student_id'] = 'str:%s' % uuid.uuid4()
        form = StudentModelForm(request_data, school_id=school_id)
        if form.is_valid():
            form.instance.stu_class = stu_class_obj
            form.instance.grade = grade_obj
            form.save()
            return redirect(self.reverse_list_url())
        return render(request, 'tables/add_student.html', {'form': form, 'school_id': school_id})

    def add_teacher(self, request, school_id):
        if request.method == 'GET':
            form = TeacherModelForm(school_id=school_id)
            return render(request, 'tables/teacher_change.html', {'form': form, 'school_id': school_id})
        form = TeacherModelForm(request.POST, school_id=school_id)
        if form.is_valid():
            form.instance.school_id = school_id
            form.instance.full_name = request.POST.get('last_name') + request.POST.get('first_name')
            teacher_obj = form.save()
            class_ids = request.POST.getlist('choice_class')
            create_list = []
            for item_id in class_ids:
                obj = tea_models.ClassToTeacher(teacher=teacher_obj, stu_class_id=item_id, relate=2)
                create_list.append(obj)
            tea_models.ClassToTeacher.objects.bulk_create(create_list)
            return redirect(self.reverse_list_url())
        return render(request, 'tables/teacher_change.html', {'form': form, 'school_id': school_id})

    def add_view(self, request, template='stark/change.html', *args, **kwargs):
        return super().add_view(request, template='tables/add_school.html', *args, **kwargs)

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        return super().change_view(request, pk, template='tables/edit_school.html', *args, **kwargs)

    search_list = ['school_name']
    list_display = [display_school_name, 'school_type', 'school_layer', display_address, display_operation]


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
