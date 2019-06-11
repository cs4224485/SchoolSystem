import copy
import os
import xlrd
import mimetypes
from django.utils.safestring import mark_safe
from Django_apps.web.forms.student_form import StudentEditForm
from django.conf import settings
from utils.common import *
from utils.checkinfo import *
from django.shortcuts import render, redirect
from Django_apps.web.forms.student_form import StudentModelForm
from django.urls import re_path
from stark.service.stark import StarkConfig
from django.http import FileResponse
from school.models import StuClass, Grade


class StudentConfig(StarkConfig):

    def get_extra_content(self, *args, **kwargs):
        return 'filter_student'

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        return StudentEditForm

    def get_queryset(self, request, *args, **kwargs):
        school_id = request.GET.get('school')
        grade_id = request.GET.get('grade')
        _class = request.GET.get('_class')
        filter_condition = {}
        if school_id:
            filter_condition['school_id'] = school_id
        if grade_id:
            filter_condition['grade_id'] = grade_id
        if _class:
            filter_condition['stu_class_id'] = _class
        return self.model_class.objects.filter(**filter_condition)

    def get_form(self, model_form, request, modify=False, *args, **kwargs):
        if modify:
            obj = kwargs.get('obj')
            request_data = copy.deepcopy(request.POST)
            stu_class_obj = StuClass.objects.filter(id=request.POST.get('stu_class')).first()
            grade_obj = Grade.objects.filter(id=request.POST.get('grade')).first()
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

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        return super(StudentConfig, self).change_view(request, pk, template='tables/edit_student.html', *args, **kwargs)

    def get_urls(self):
        urlpatterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^(?P<pk>\d+)/change/', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path(r'^(?P<pk>\d+)/del/', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())
        return urlpatterns

    def get_list_display(self):
        val = super().get_list_display()
        return val

    def display_stu_class(self, row=None, header=False, *args, **kwargs):
        if header:
            return '班级'
        return "%s(%s届)" % (row.stu_class, row.period)

    def get_add_btn(self):
        return None

    def display_name(self, row=None, header=False, *args, **kwargs):
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


class SchoolStudentConfig(StudentConfig):
    '''
    每个学校的学生信息
    '''

    change_list_template = 'student_list.html'

    def get_urls(self):
        urlpatterns = [
            re_path(r'^list/(?P<school_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^import_student/(?P<school_id>\d+)/$', self.wrapper(self.import_student), name='import_student'),
            re_path(r'^add_student/(?P<school_id>\d+)/$', self.wrapper(self.add_student), name='add_student'),
            re_path(r'^change/(?P<school_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_edit_url_name),
            re_path(r'^del/(?P<school_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view),
                    name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())

        return urlpatterns

    def extra_urls(self):
        url = [re_path('^tpl/$', self.wrapper(self.student_tpl), name='tpl_student')]
        return url

    def get_queryset(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        grade_id = request.GET.get('grade')
        _class = request.GET.get('_class')
        filter_condition = {'school_id': school_id}
        if grade_id:
            filter_condition['grade_id'] = grade_id
        if _class:
            filter_condition['stu_class_id'] = _class
        return self.model_class.objects.filter(**filter_condition)

    def get_extra_content(self, *args, **kwargs):
        add_student_url = self.reverse_commons_url('add_student', *args, **kwargs)
        import_student_url = self.reverse_commons_url('import_student', *args, **kwargs)
        return {'add': add_student_url, 'import': import_student_url}

    def get_list_display(self):
        display_list = []
        display_list.extend(self.list_display)
        display_list.append(StarkConfig.display_edit_del)
        return display_list

    def import_student(self, request, school_id, *args, **kwargs):
        '''
        通过excel导入学生
        :param request:
        :param args:
        :param kwargs:
        :param school_id:学校ID
        :return:
        '''
        if request.method == 'GET':
            tpl_url = self.reverse_commons_url('tpl_student', *args, **kwargs)
            return render(request, 'tables/student_import.html', {'url': tpl_url})

        context = {'status': True, 'msg': '导入成功'}
        try:
            student_excel = request.FILES.get('student_excel')
            """
            打开上传的Excel文件，并读取内容
            注：打开本地文件时，可以使用：workbook = xlrd.open_workbook(filename='本地文件路径.xlsx')
            """
            workbook = xlrd.open_workbook(file_contents=student_excel.file.read())

            # sheet = workbook.sheet_by_name('工作表1')
            sheet = workbook.sheet_by_index(0)
            row_map = {
                0: {'text': '姓名', 'name': 'full_name'},
                1: {'text': '姓', 'name': 'last_name'},
                2: {'text': '名', 'name': 'first_name'},
                3: {'text': '出生日期', 'name': 'birthday'},
                4: {'text': '学号', 'name': 'student_id'},
                5: {'text': '班级', 'name': 'stu_class'},
                6: {'text': '年级', 'name': 'grade'},
                7: {'text': '学籍号', 'name': 'student_code'},
                8: {'text': '身份证号码', 'name': 'id_card'},
                9: {'text': '性别', 'name': 'gender'}
            }
            object_list = []
            for row_num in range(1, sheet.nrows):
                row = sheet.row(row_num)
                row_dict = {}
                for col_num, name_text in row_map.items():
                    ctype = sheet.cell(row_num, col_num).ctype  # 表格数据类型
                    cell = sheet.cell_value(row_num, col_num)
                    if col_num == 6:
                        row_dict['grade'] = Grade.objects.filter(grade_name=row[6].value).first()
                        row_dict['stu_class'] = StuClass.objects.filter(name=row[5].value,
                                                                        grade=row_dict['grade'],
                                                                        school=school_id).first()
                        # 届别
                        row_dict['period'] = calculate_period(row_dict['grade'].get_grade_name_display())
                        continue
                    elif col_num == 5:
                        continue
                    elif ctype == 3:
                        date = datetime.datetime(*xlrd.xldate_as_tuple(cell, 0))
                        row[3].value = date.strftime('%Y-%m-%d')
                    row_dict[name_text['name']] = row[col_num].value
                # 所在学校
                row_dict['school'] = SchoolInfo.objects.filter(pk=school_id).first()
                # 学生内部ID
                row_dict['interior_student_id'] = 'str:%s' % uuid.uuid4()

                # 根据身份证计算信息
                id_card = row[8].value
                # 学籍号
                row_dict['student_code'] = row[7].value if row[7].value else None
                # 生日
                row_dict['birthday'] = row[3].value

                if id_card:
                    is_exist = check_id_exist(id_card)
                    # if is_exist:
                    #     continue
                    # 对身份证进行合法性校验
                    check_state, info = check_id_card(id_card)
                    if not check_state:
                        continue
                    row_dict['birthday'] = info['birthday']
                    row_dict['gender'] = info['gender'][0]
                # 如果有生日计算日龄 生肖 年龄等信息
                if row_dict['birthday']:
                    y, m, d = row_dict['birthday'].split('-')
                    row_dict['constellation'] = get_constellation(int(m), int(d))[0]
                    row_dict['age'] = calculate_age(int(y))
                    row_dict['day_age'] = calculate_day_age(int(y), int(m), int(d))
                    row_dict['chinese_zodiac'] = get_ChineseZodiac(int(y))[0]
                student_obj = StudentInfo.objects.filter(full_name=row_dict['full_name'], school_id=school_id,
                                                         birthday=row_dict['birthday'])
                if not row_dict['gender']: row_dict['gender'] = None
                if student_obj:
                    row_dict.pop('interior_student_id')
                    student_obj.update(**row_dict)
                    continue
                object_list.append(StudentInfo(**row_dict))
            StudentInfo.objects.bulk_create(object_list, batch_size=20)
        except Exception as e:
            print(e)
            context['status'] = False
            context['msg'] = '导入失败'

        return render(request, 'tables/student_import.html', context)

    def student_tpl(self, request):
        """
        下载批量导入Excel列表
        :param request:
        :return:
        """
        tpl_path = os.path.join(settings.BASE_DIR, 'Django_apps', 'web', 'files', '学生导入格式模板.xls')
        content_type = mimetypes.guess_type(tpl_path)[0]
        response = FileResponse(open(tpl_path, mode='rb'), content_type=content_type)
        response['Content-Disposition'] = "attachment;filename=%s" % 'student_excel_tpl.xls'
        return response

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
        stu_class_obj = StuClass.objects.filter(id=request.POST.get('stu_class')).first()
        grade_obj = Grade.objects.filter(id=request.POST.get('grade')).first()
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
            return redirect(self.reverse_commons_url('students_studentinfo_school_list', school_id=school_id))
        return render(request, 'tables/add_student.html', {'form': form, 'school_id': school_id})
