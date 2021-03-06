'''
学校相关信息
'''
import json
from django import views
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse
from school import models as sc_models
from teacher import models as tea_models
from utils.base_response import BaseResponse
from utils.generate_calender import *
from school.service.course_service import CourseService


class ClassManage(views.View):
    '''
    学校班级管理信息
    '''

    def get(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        school_obj = sc_models.SchoolInfo.objects.filter(id=school_id).only('school_name').first()
        class_queryset = order_by_class(list(sc_models.StuClass.objects.filter(school=school_obj).order_by('grade')))
        teacher_list = tea_models.TeacherInfo.objects.filter(school=school_obj, identity=2)
        class_dict = {}
        for item in class_queryset:
            grade_id = item.grade_id
            per_class_student = item.student_class.all().count()
            class_name = item.name
            tutor = tea_models.ClassToTeacher.objects.filter(stu_class_id=item.id, relate=1).order_by('-create_date',
                                                                                                      '-id').first()
            children_dict = {
                'per_class_student': per_class_student,
                'class_name': class_name,
                'class_id': item.id,
                'tutor': tutor.teacher.last_name + tutor.teacher.first_name if tutor else None,
                'tutor_id': tutor.teacher.id if tutor else 0
            }
            if grade_id not in class_dict:
                period = calculate_period(item.grade.get_grade_name_display())
                class_dict[grade_id] = {
                    'class_total_student': per_class_student,
                    'total_class': 1,
                    'grade_id': grade_id,
                    'grade': item.grade.get_grade_name_display(),
                    'peroid': period,
                    'children': [children_dict]
                }
            else:
                class_dict[grade_id]['total_class'] += 1
                class_dict[grade_id]['class_total_student'] += per_class_student
                class_dict[grade_id]['children'].append(children_dict)
        return render(request, 'school_info/class_manage.html',
                      {'class_dict': class_dict, 'school_obj': school_obj, 'teacher_list': teacher_list})

    def patch(self, request, *args, **kwargs):
        '''
        添加一个班级
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ret = BaseResponse()
        try:
            data = json.loads(request.body.decode('utf-8'))
            grade_id = data.get('grade')
            class_name = data.get('className')
            school_id = kwargs.get('school_id')
            class_obj = sc_models.StuClass.objects.filter(grade_id=grade_id, school_id=school_id,
                                                          name=class_name).first()
            if class_obj:
                ret.msg = '该班级以存在'
                return JsonResponse(ret.get_dict)
            class_obj = sc_models.StuClass.objects.create(grade_id=grade_id, school_id=school_id, name=class_name)
            ret.state = True
            ret.msg = '创建成功'
            ret.data = {'class_id': class_obj.id}
        except Exception as e:
            print(e)
            ret.msg = '创建失败'
        return JsonResponse(ret.get_dict)

    def post(self, request, *args, **kwargs):
        '''
        更新班级名称以及对应的班主任
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        ret = BaseResponse()
        try:
            data = json.loads(request.body.decode('utf-8'))
            teacher_id = data.get('teacherId')
            class_name = data.get('className')
            class_id = data.get('classId', 0)
            # 修改编辑名称操作
            class_obj = sc_models.StuClass.objects.filter(id=class_id).only('name').first()
            if class_name != class_obj.name:
                sc_models.StuClass.objects.filter(id=class_id).update(name=class_name)
            if teacher_id:
                class_tutor_obj = tea_models.ClassToTeacher.objects.filter(stu_class_id=class_id, relate=1)
                if class_tutor_obj:
                    class_tutor_obj.update(teacher_id=teacher_id)
                else:
                    tea_models.ClassToTeacher.objects.create(teacher_id=teacher_id, stu_class_id=class_id)
            ret.msg = '修改成功'
            ret.state = True
        except Exception as e:
            print(e)
            ret.msg = '修改失败'
        return JsonResponse(ret.get_dict)


class SchoolCalender(views.View):
    '''
    学校校历
    '''

    def get(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        school_obj = sc_models.SchoolInfo.objects.filter(id=school_id).only('school_name').first()
        cal_obj = CalenderHandler()
        month_day_num = cal_obj.get_per_month_day()
        cal_des_options = sc_models.SchoolCalendar.des_choice
        years = list(month_day_num.keys())
        # 年度
        school_year = '%s-%s年度' % (years[0], years[1])
        # 获取校历描述信息
        school_special_day = sc_models.SchoolCalendar.objects.filter(school_id=school_id).all()

        special_day_dict = {}
        for special in school_special_day:
            day_des = special.get_date_des_display()
            node = {'id': special.id,
                    'des': day_des,
                    'des_id': special.date_des,
                    'end_date': ''}
            if day_des == '开学' or day_des == '寒假' or day_des == '暑假' or not special.end_date:
                special_day_dict[special.date] = node
            else:
                node['end_date'] = special.end_date
                special_day_dict[special.date] = node
        return render(request, 'school_info/school_calender.html',
                      {'school_obj': school_obj, 'month_day_num': month_day_num, 'cal_des_options': cal_des_options,
                       'school_year': school_year, 'special_day': special_day_dict})

    def post(self, request, *args, **kwargs):

        '''
        提交日期对应的描述
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        res = BaseResponse()
        try:
            school_id = kwargs.get('school_id')
            start_date = request.POST.get('startDate')
            end_data = request.POST.get('endDate')
            des_ops = request.POST.get('desOptions')
            calendar_id = request.POST.get('specialId')
            save_data = {
                'date': start_date,
                'date_des': des_ops,
                'school_id': school_id
            }
            if end_data:
                if datetime.datetime.strptime(start_date, '%Y-%m-%d') > datetime.datetime.strptime(end_data,
                                                                                                   '%Y-%m-%d'):
                    res.msg = '结束日期要在开始日期之后'
                    return JsonResponse(res.get_dict)
                save_data['end_date'] = end_data
            if calendar_id:
                calendar_obj = sc_models.SchoolCalendar.objects.filter(id=calendar_id)
                if calendar_obj:
                    calendar_obj.update(**save_data)
                    res.msg = '修改成功'
            else:
                sc_models.SchoolCalendar.objects.create(**save_data)
                res.msg = '创建成功'
            res.state = True
        except Exception as e:
            print(e)
            res.msg = '创建失败'
        return JsonResponse(res.get_dict)


class SchoolTimeTable(views.View):
    '''
    学校课程表
    '''

    def get(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        grade = request.GET.get('gradeId', 7)
        service_obj = CourseService(school_id, grade)
        course_data = service_obj.create_course_data()
        return render(request, 'school_info/school_timetable.html', course_data)

    def post(self, request, *args, **kwargs):
        '''
        添加一个课程表记录
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        res = BaseResponse()

        try:
            time_info = request.POST.get('timeInfo')
            school_id = kwargs.get('school_id')
            time_obj = sc_models.SchoolTimeRange.objects.filter(start_time=time_info, school_id=school_id).first()
            week = request.POST.get('week')
            # 课程表Id 如果存在表示需要更新不存在则创建
            course_table_id = request.POST.get('courseTableId')
            record_type = int(request.POST.get('type'))
            table_query = sc_models.SchoolTimetable.objects

            if not time_obj:
                res.msg = '请先设置时间'
                return JsonResponse(res.get_dict)

            # 代表添加的是普通的课程
            if record_type == 0:
                teacher_id = request.POST.get('teacherId')
                course_id = request.POST.get('courseId')
                class_id = request.POST.get('classId')
                class_obj = sc_models.StuClass.objects.filter(id=class_id).first()
                # 单双周信息
                course_week = request.POST.get('singleDoubleWeek')
                if not class_obj:
                    res.msg = '该班级不存在'
                    return JsonResponse(res.get_dict)

                teacher_obj = tea_models.TeacherInfo.objects.filter(id=teacher_id).first()
                if not teacher_obj:
                    res.msg = '该教师已不存在, 请刷新页面'
                    return JsonResponse(res.get_dict)
                course_table_obj = table_query.filter(week=week, time_range=time_obj,
                                                      stu_class=class_id)
                if course_table_obj and not course_week and not course_table_id:
                    res.msg = "该时段课程已存在,请重新核对或选择单双周"
                    return JsonResponse(res.get_dict)

                course_obj = sc_models.Course.objects.filter(id=course_id).first()
                if not course_obj:
                    res.msg = '该课程已不存在, 请刷新页面'
                    return JsonResponse(res.get_dict)
                save_dict = {
                    'stu_class_id': class_id,
                    'course': course_obj,
                    'week': week,
                    'school_id': school_id,
                    'time_range': time_obj,
                    'teacher': teacher_obj,
                    'single_double_week': course_week
                }
                if int(course_week) == 1:
                    filter_dic = {'time_range': time_obj, 'single_double_week__in': [2, 3]}
                    # 如果单周或双周改为每周 要把对应单元格另外的一个单双周数据删除
                    if course_table_id:
                        table_query.filter(**filter_dic).exclude(id=course_table_id).delete()
                    else:
                        table_query.filter(**filter_dic).delete()

                else:
                    table_obj = table_query.filter(time_range=time_obj, single_double_week=course_week)
                    if table_obj:
                        table_obj.delete()

            # 代表添加的是其他事件
            elif record_type == 1:
                event_id = request.POST.get('event')
                save_dict = {
                    'week': week,
                    'school_id': school_id,
                    'time_range': time_obj,
                    'other_event': int(event_id),
                    'info_type': 2
                }
            else:
                raise Exception
            if course_table_id:
                obj = table_query.filter(id=course_table_id)
                if record_type == 0:
                    obj.update(info_type=1, other_event=None)
                obj.update(**save_dict)
                obj = obj.first()
                res.msg = '修改成功'
            else:
                obj = table_query.create(**save_dict)

            # 添加或修改成功后将需要的数据返回给前端
            if obj:
                if obj.info_type == 1:
                    result_data = {
                        'table_id': obj.id,
                        'course_id': obj.course.id,
                        'course_name': obj.course.course_des,
                        'teacher_id': obj.teacher.id,
                        'teacher_name': obj.teacher.last_name + obj.teacher.first_name,
                        'course_week': int(obj.single_double_week),
                        'info_type': 0
                    }
                else:
                    result_data = {
                        'table_id': obj.id,
                        'event_id': obj.other_event,
                        'event_name': obj.get_other_event_display(),
                        'info_type': 1
                    }
                res.msg = '添加成功'
                res.data = result_data
                res.state = True
        except Exception as e:
            print(e)
            res.msg = '添加失败'

        return JsonResponse(res.get_dict)

    def patch(self, request, *args, **kwargs):
        '''
        更新课程表对应的时间
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        res = BaseResponse()
        try:
            data = json.loads(request.body.decode('utf-8'))
            start_time = data.get('time')
            # 原来的时间
            source_time = data.get('sourceTime', '')
            school_id = kwargs.get('school_id')
            query = sc_models.SchoolTimeRange.objects

            is_exist = query.filter(start_time=start_time, school_id=school_id).first()
            if is_exist:
                res.code = -1
                res.msg = '该时间段已经存在，请重新编辑'
                return JsonResponse(res.get_dict)
            if not source_time:
                # 没有原来设置的时间添加操作
                query.create(start_time=start_time, school_id=school_id)
            else:
                # 如果有原来设置的时间更新操作
                query.filter(start_time=source_time, school_id=school_id).update(start_time=start_time)
            res.state = True
            res.code = 200
        except:
            res.code = -1
            res.msg = '编辑时间失败请重新编辑'
        return JsonResponse(res.get_dict)

    def delete(self, request, *args, **kwargs):
        '''
        根据时间删除一行课程数据表
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        res = BaseResponse()
        try:
            data = json.loads(request.body.decode('utf-8'))
            school_id = kwargs.get('school_id')
            start_time = data.get('time')
            time_obj = sc_models.SchoolTimeRange.objects.filter(start_time=start_time, school_id=school_id)
            sc_models.SchoolTimetable.objects.filter(time_range=time_obj.first()).delete()
            time_obj.delete()
            res.code = 200
            res.state = True
        except Exception as e:
            res.code = -1
            res.msg = '删除失败'
        return JsonResponse(res.get_dict)