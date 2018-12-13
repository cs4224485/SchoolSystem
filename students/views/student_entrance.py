# Create your views here
import json
import xlrd
from utils.common import *
from utils.checkinfo import *
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django import views
from school import models as sc_models
from students import models as stu_models


class StudentInfo(views.View):
    '''
    跳转学生填表页面
    '''

    start_time = []

    def get(self, request, nid, *args, **kwargs):
        step = request.GET.get('step', 'start_page')
        setting_obj = sc_models.TableSettings.objects.filter(id=nid).first()
        result = self.check(setting_obj)
        if result:
            return result
        self.start_time.append(time.time())
        if hasattr(self, step):
            func = getattr(self, step)
            return func(request, setting_obj)

    def post(self, request, nid, *args, **kwargs):
        self.message = {
            'state': False,
            'msg': '',
            'data': []
        }
        stu_name = request.POST.get('name')
        birthday = request.POST.get('birthday')
        grade = request.POST.get('classes')
        stu_class = request.POST.get('classess')
        stu_obj = stu_models.StudentInfo.objects.filter(full_name=stu_name, birthday=birthday, grade=grade,
                                                        stu_class=stu_class).first()

        setting_obj = sc_models.TableSettings.objects.filter(id=nid).first()

        if not stu_obj:
            self.message['msg'] = '您好，你所填学生信息与学校记录不符，请查证后再填'
            return JsonResponse(self.message)
        else:
            table_info = sc_models.TableInfo.objects.filter(table=setting_obj, student=stu_obj)
            if table_info:
                self.message['msg'] = '该学生已填写完成,无法再次填写'
                return JsonResponse(self.message)
            self.message['state'] = True
            self.message['student_id'] = stu_obj.pk
            return JsonResponse(self.message)

    def check(self, setting_obj):
        if not setting_obj:
            return HttpResponse('该表单不存在或已过期')
        start_time = setting_obj.stat_time
        end_time = setting_obj.end_time
        current_time = datetime.date.today()
        if current_time < start_time:
            return HttpResponse('填表时间还未开始')
        if end_time:
            if current_time > end_time:
                return HttpResponse('填表已结束')

    def start_page(self, request, setting_obj):
        school_obj = setting_obj.school_range.first()
        return render(request, 'entrance/landing.html', {'setting_obj': setting_obj, 'school_obj': school_obj})

    def stu_info_page(self, request, setting_obj):
        school_obj = setting_obj.school_range.first()
        student_id = request.GET.get('student_id')
        if not student_id:
            self.message['msg'] = '您好，请先填写登陆页面'
            return JsonResponse(self.message)
        student_obj = stu_models.StudentInfo.objects.filter(id=student_id).first()
        stu_field_list = sc_models.SettingToField.objects.order_by('order').filter(setting=setting_obj,
                                                                                   fields__field_type=1).values(
            'fields__fieldName', 'fields__pk')
        if stu_field_list:
            return render(request, 'entrance/student_info.html',
                          {'stu_field_list': stu_field_list, 'pk': setting_obj.pk, 'student_obj': student_obj,
                           'school_obj': school_obj})
        return self.health_page(request, setting_obj)

    def health_page(self, request, setting_obj):
        hel_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=2).values(
            'fields__fieldName', 'fields__pk')
        if hel_field_list:
            return render(request, 'entrance/health_info.html',
                          {'hel_field_list': hel_field_list, 'pk': setting_obj.pk})
        return self.family_page(request, setting_obj)

    def family_page(self, request, setting_obj):
        fam_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=3).values(
            'fields__fieldName', 'fields__pk')
        if fam_field_list:
            school_district = setting_obj.school_range.values('province', 'city', 'region').first()
            return render(request, 'entrance/family_info.html',
                          {'fam_field_list': fam_field_list, 'pk': setting_obj.pk,
                           'school_district': json.dumps(school_district)})
        return self.parents_page(request, setting_obj)

    def parents_page(self, request, setting_obj):
        par_field_list = sc_models.SettingToField.objects.filter(setting=setting_obj, fields__field_type=4).values(
            'fields__fieldName', 'fields__pk')

        if par_field_list:
            par_field_json = []
            for item in par_field_list:
                par_field_json.append(item.get('fields__fieldName'))
            return render(request, 'entrance/parent_info.html',
                          {'fam_field_list': par_field_list, 'pk': setting_obj.pk,
                           'par_field_json': json.dumps(par_field_json)})

        return self.question_page(request, setting_obj)

    def question_page(self, request, setting_obj):
        # 自定制问题页面, 如矩阵列表,单选多选
        scale_list = setting_obj.scale.all()
        single_choice_list = setting_obj.choice.filter(choice_type=1)
        multi_choice_list = setting_obj.choice.filter(choice_type=2)

        if scale_list or single_choice_list:
            return render(request, 'entrance/questions.html', {'scale_list': scale_list, 'pk': setting_obj.pk,
                                                               'single_choice_list': single_choice_list,
                                                               'multi_choice_list': multi_choice_list})
        return self.finish_page(request, setting_obj)

    def finish_page(self, request, setting_obj):
        student_id = request.GET.get('student_id')
        end_time = time.time() - self.start_time[0]
        sc_models.TableInfo.objects.create(table=setting_obj, finish_time=int(end_time), student_id=student_id)
        return render(request, 'entrance/table_finish.html')


class ImportStudent(views.View):
    '''
    通过excel导入学生信息
    '''

    def get(self, request, school_id, *args, **kwargs):
        return render(request, 'operation_table/student_import.html')

    def post(self, request, school_id, *args, **kwargs):
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
                0: {'text': '年级', 'name': 'grade'},
                1: {'text': '班级', 'name': 'stu_class'},
                2: {'text': '姓', 'name': 'last_name'},
                3: {'text': '名', 'name': 'first_name'},
                4: {'text': '学籍辅号', 'name': 'student_code'},
                5: {'text': '身份证号码', 'name': 'id_card'},
            }
            object_list = []
            for row_num in range(1, sheet.nrows):
                row = sheet.row(row_num)
                row_dict = {}
                for col_num, name_text in row_map.items():
                    if col_num == 0:
                        row_dict['grade'] = sc_models.Grade.objects.filter(grade_name=row[0].value).first()
                        row_dict['stu_class'] = sc_models.StuClass.objects.filter(name=row[1].value,
                                                                                  grade=row_dict['grade']).first()
                        # 届别
                        row_dict['period'] = calculate_period(row_dict['grade'].get_grade_name_display())
                        continue
                    elif col_num == 1:
                        continue
                    row_dict[name_text['name']] = row[col_num].value
                # 学生全名
                row_dict['full_name'] = row[2].value + row[3].value
                # 所在学校
                row_dict['school'] = sc_models.SchoolInfo.objects.filter(pk=school_id).first()
                # 学生内部ID
                import uuid
                row_dict['interior_student_id'] = 'str:%s' % uuid.uuid4()
                # 根据身份证计算信息
                id_card = row[5].value
                if id_card:
                    is_exist = check_id_exist(id_card)
                    if is_exist:
                        continue
                    # 对身份证进行合法性校验
                    check_state, info = check_id_card(id_card)
                    if not check_state:
                        pass
                    row_dict['birthday'] = info['birthday']
                    row_dict['gender'] = info['gender'][0]
                    if row_dict['birthday']:
                        y, m, d = row_dict['birthday'].split('-')
                        row_dict['constellation'] = get_constellation(int(m), int(d))[0]
                        row_dict['age'] = calculate_age(int(y))
                        row_dict['day_age'] = calculate_day_age(int(y), int(m), int(d))
                        row_dict['chinese_zodiac'] = get_ChineseZodiac(int(y))[0]
                object_list.append(stu_models.StudentInfo(**row_dict))
            stu_models.StudentInfo.objects.bulk_create(object_list, batch_size=20)
        except Exception as e:
            context['status'] = False
            context['msg'] = '导入失败'

        return render(request, 'operation_table/student_import.html', context)
