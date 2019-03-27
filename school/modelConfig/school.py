import copy
from stark.service.stark import StarkConfig, ChangeList
from django.urls import reverse, re_path
from django.conf import settings
from django.utils.safestring import mark_safe
from school import models
from school.views import school_information
from school.forms.school import SchoolAddForm, SchoolEditModelForm


class SchoolInfoConfig(StarkConfig):

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
        student_url = self.reverse_commons_url('students_studentinfo_school_list', school_id=row.pk)
        teacher_url = self.reverse_commons_url('teacher_teacherinfo_school_list', school_id=row.pk)
        class_manage_url = self.reverse_commons_url('class_manage', row.pk)
        calender_url = self.reverse_commons_url('school_calender', row.pk)
        course_tbale_url = self.reverse_commons_url('school_timetables', row.pk)
        html = '''
            <div class='op_father'>
                <span><image src="/static/stark/imgs/op.png" width="18" height="18"></span>  
                <div class='op_list'>
                    <a href='%s'>编辑学校</a>
                    <a href='%s'>学生管理</a>
                    <a href='%s'>教师管理</a>
                    <a href='%s'>班级管理</a>
                    <a href='%s'>学校校历</a>
                    <a href='%s'>课程表</a>
                </div>
            </div>
        ''' % (edit_school_url, student_url,
               teacher_url, class_manage_url, calender_url, course_tbale_url)
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

    def add_view(self, request, template='stark/change.html', *args, **kwargs):
        return super().add_view(request, template='tables/add_school.html', *args, **kwargs)

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        return super().change_view(request, pk, template='tables/edit_school.html', *args, **kwargs)

    search_list = ['school_name']
    list_display = [display_school_name, 'school_type', 'school_layer', display_address, display_operation]


class ChoiceFieldConfig(StarkConfig):
    list_display = ['fieldName', 'field_english', 'field_type']


class SettingToFieldConfig(StarkConfig):
    list_display = ['setting', 'fields', 'order']
