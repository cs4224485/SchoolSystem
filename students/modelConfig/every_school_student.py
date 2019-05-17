import copy
import xlrd, datetime
from utils.common import *
from utils.checkinfo import *
from django.shortcuts import render, redirect
from school import models as sc_models
from students import models as stu_models
from students.forms.student_form import StudentModelForm
from students.modelConfig.student import StudentConfig
from django.urls import re_path
from stark.service.stark import StarkConfig


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

    def get_queryset(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        return self.model_class.objects.filter(school_id=school_id)

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
            return render(request, 'tables/student_import.html')

        context = {'status': True, 'msg': '导入成功'}
        # try:
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
        }
        object_list = []
        for row_num in range(1, sheet.nrows):
            row = sheet.row(row_num)
            row_dict = {}
            for col_num, name_text in row_map.items():
                ctype = sheet.cell(row_num, col_num).ctype  # 表格数据类型
                cell = sheet.cell_value(row_num, col_num)
                if col_num == 6:
                    row_dict['grade'] = sc_models.Grade.objects.filter(grade_name=row[6].value).first()
                    row_dict['stu_class'] = sc_models.StuClass.objects.filter(name=row[5].value,
                                                                              grade=row_dict['grade']).first()
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
            row_dict['school'] = sc_models.SchoolInfo.objects.filter(pk=school_id).first()
            # 学生内部ID
            import uuid
            row_dict['interior_student_id'] = 'str:%s' % uuid.uuid4()
            # 根据身份证计算信息
            id_card = row[8].value
            # 学籍号
            row_dict['student_code'] = row[7].value if row[7].value else None
            # 生日
            row_dict['birthday'] = row[3].value

            if id_card:
                is_exist = check_id_exist(id_card)
                if is_exist:
                    continue
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
            print(row_dict)
            object_list.append(stu_models.StudentInfo(**row_dict))
        stu_models.StudentInfo.objects.bulk_create(object_list, batch_size=20)
        # except Exception as e:
        #     context['status'] = False
        #     context['msg'] = '导入失败'
        #     print(e)
        return render(request, 'tables/student_import.html', context)

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
        stu_class_obj = sc_models.StuClass.objects.filter(id=request.POST.get('stu_class')).first()
        grade_obj = sc_models.Grade.objects.filter(id=request.POST.get('grade')).first()
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
