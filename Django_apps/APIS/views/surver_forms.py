from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView, Response
from school.models import ScaleSetting, SchoolInfo, StuClass, Grade, ScaleOptionDes, ScaleLineTitle, TableInfo
from Django_apps.students.models import StudentInfo, ScaleQuestion, ScaleValue
from APIS.serialize.surver_form import SchoolSerializers, GradeSerializers, ClassSerializers, StudentSerializers, \
    StudentDetailSerializes
from utils.base_response import BaseResponse
from utils.common import order_by_class
import pandas as pd


class SchoolInfoViewSet(APIView):

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        school_id = request.query_params.get('school_id')
        try:
            if not school_id:
                res.code = 403
                res.msg = '请提供学校id'
                return Response(res.get_dict)
            school_obj = SchoolInfo.objects.filter(id=school_id).first()
            if not school_obj:
                res.code = 404
                res.msg = '该学校不存在'
                return Response(res.get_dict)
            school_se = SchoolSerializers(school_obj)
            res.data = {'school': school_se.data}
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = '获取错误'
        return Response(res.get_dict)


class GradeAndClassViewSet(APIView):
    '''
    获取班级或者年级
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        school_id = request.query_params.get('school_id')
        grade = request.query_params.get('grade')
        try:
            if not school_id:
                res.code = 403
                res.msg = '请提供学校id'
                return Response(res.get_dict)

            if not grade:
                grade_queryset = Grade.objects.filter(stuclass__school_id=school_id).all().distinct()
                grade_se = GradeSerializers(grade_queryset, many=True)
                res.data = {'grade': grade_se.data}
                res.code = 200
            else:
                class_queryset = list(StuClass.objects.filter(grade=grade, school_id=school_id).all().distinct())
                class_queryset = order_by_class(class_queryset)
                class_se = ClassSerializers(class_queryset, many=True)
                res.data = {'_class': class_se.data}
                res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = '获取失败'
        return Response(res.get_dict)


class PerClassStudentListViewSet(APIView):
    '''
    每个班级学生列表
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            class_id = request.query_params.get('class_id')
            if not class_id:
                res.code = 403
                res.msg = "请提供班级ID"
                return Response(res.get_dict)

            student_list = StudentInfo.objects.filter(stu_class_id=class_id).values('full_name', 'id').distinct()
            student_se = StudentSerializers(student_list, many=True)
            res.code = 200
            res.data = {'students': student_se.data}
        except Exception as e:
            res.code = 500
            res.msg = "获取错误"
        return Response(res.get_dict)


class StudentScaleAvgViewSet(APIView):
    '''
    获取学生以及学生所在班级和年级量表信息的平均值
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            school_id = request.query_params.get('school_id')
            table_id = request.query_params.get('table_id')
            student_id = request.query_params.get('student_id')

            if not student_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)
            if not table_id:
                res.code = 403
                res.msg = '请提供表单ID'
                return Response(res.get_dict)
            if not school_id:
                res.code = 403
                res.msg = '请提供学校id'
                return Response(res.get_dict)
            table_info = TableInfo.objects.filter(student_id=student_id, table_id=table_id).first()
            student_obj = StudentInfo.objects.filter(id=student_id).first()
            if not student_obj:
                res.code = 404
                res.msg = '该学生不存在'
                return Response(res.get_dict)
            if not table_info:
                res.code = 403
                res.msg = '暂无数据'
                return Response(res.get_dict)
            class_obj = student_obj.stu_class
            grade_obj = student_obj.grade
            scale_queryset = ScaleSetting.objects.filter(setting_table=table_id).all()
            # 年级量表信息
            grade_scale_data_list = []
            # 学生量表信息
            student_scale_data_list = []
            # 班级量表信息
            class_scale_data_list = []
            # 表单中每个量表返回一个生成器 循环生成器取出每个量表相关信息
            scale_generator = per_scale_info(scale_queryset)
            for scale_obj, scale_line_title, scale_line_value_des in scale_generator:
                scale_query = ScaleQuestion.objects
                # 学生个人量表数据
                student_scale = scale_query.filter(scale=scale_obj, student__school_id=school_id,
                                                   student_id=student_id)
                # 班级量表数据
                class_scale = scale_query.filter(scale=scale_obj, student__stu_class=class_obj)
                # 年级量表数据
                grade_scale = scale_query.filter(scale=scale_obj, student__grade=grade_obj)
                student_pd = get_scale_value(student_scale, scale_line_value_des,
                                             pd.DataFrame(columns=scale_line_title))
                grade_pd = get_scale_value(grade_scale, scale_line_value_des, pd.DataFrame(columns=scale_line_title))
                class_pd = get_scale_value(class_scale, scale_line_value_des, pd.DataFrame(columns=scale_line_title))
                grade_scale_data_list.append(grade_pd)
                class_scale_data_list.append(class_pd)
                student_scale_data_list.append(student_pd)
            student_data = calculate_arg_by_pd_col(student_scale_data_list)
            class_avg = calculate_arg_by_pd_col(class_scale_data_list)
            grade_avg = calculate_arg_by_pd_col(grade_scale_data_list)
            res.data = {'class_avg': class_avg, 'grade_avg': grade_avg, 'student_data': student_data}
            res.code = 200
        except Exception as e:
            print(e)
            res.code = 500
            res.msg = '获取错误'
        return Response(res.get_dict)


class SchoolScaleAvgViewSet(APIView):
    '''
    获取全校学生填写量表的平均值
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        school_id = request.query_params.get('school_id')
        table_id = request.query_params.get('table_id')

        if not table_id:
            res.code = 403
            res.msg = '请提供表单ID'
            return Response(res.get_dict)
        if not school_id:
            res.code = 403
            res.msg = '请提供学校id'
            return Response(res.get_dict)
        scale_queryset = ScaleSetting.objects.filter(setting_table=table_id).all()
        # 全校量表信息
        school_scale_data_list = []
        # 表单中每个量表返回一个生成器 循环生成器取出每个量表相关信息
        scale_generator = per_scale_info(scale_queryset)
        for scale_obj, scale_line_title, scale_line_value_des in scale_generator:
            # 全校所有学生量表填写情况
            scale_query = ScaleQuestion.objects
            school_scale_queryset = scale_query.filter(scale=scale_obj, student__school_id=school_id).all()
            school_pd = get_scale_value(school_scale_queryset, scale_line_value_des,
                                        pd.DataFrame(columns=scale_line_title))
            school_scale_data_list.append(school_pd)
        school_avg = calculate_arg_by_pd_col(school_scale_data_list)
        res.code = 200
        res.data = {'school_avg': school_avg}

        return Response(res.get_dict)


class TableInfoViewSet(APIView):

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        school_id = request.query_params.get('school_id')
        table_id = request.query_params.get('table_id')
        if not table_id:
            res.code = 403
            res.msg = '请提供表单ID'
            return Response(res.get_dict)
        if not school_id:
            res.code = 403
            res.msg = '请提供学校id'
            return Response(res.get_dict)
        table_info = TableInfo.objects.filter(table_id=table_id).all()
        res.data = {'title': table_info.first().table.title, 'filled_num': len(table_info)}
        res.code = 200

        return Response(res.get_dict)


class StudentDetailInfo(APIView):
    '''
    学生消息信息
    '''

    def get(self, request, *args, **kwargs):

        res = BaseResponse()
        try:
            student_id = request.query_params.get('student_id')
            if not student_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)
            student_obj = StudentInfo.objects.filter(id=student_id).first()
            student_se = StudentDetailSerializes(student_obj)
            res.data = {'student': student_se.data}
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = '获取失败'
        return Response(res.get_dict)


def per_scale_info(scale_queryset):
    '''
    循环每一张量表
    :param scale_queryset:
    :return:
    '''
    for scale_obj in scale_queryset:
        # 取出每张量表标题
        scale_line_title = [item.des for item in ScaleLineTitle.objects.filter(scale_table=scale_obj)]
        # 取出每张量表的值得描述 以便后面对应分值【1-5分】
        scale_line_value_des = [item.des for item in ScaleOptionDes.objects.filter(scale_table=scale_obj)]
        yield scale_obj, scale_line_title, scale_line_value_des


def get_scale_value(scale_queryset, scale_line_value_des, pd_data):
    '''
    获取每个学生填写量表得每一行得数据值
    :param scale_queryset:
    :param scale_line_value_des:
    :param pd_data:
    :return:
    '''
    # 每个学生填写的量表
    for student_scale in scale_queryset:
        student_name = student_scale.student.full_name
        line_value_list = []
        # 量表每一行相关的数据
        for scale in student_scale.scale_value.prefetch_related():
            line_value = scale_line_value_des.index(scale.value.des) + 1
            line_value_list.append(line_value)
        if line_value_list:
            pd_data.loc[student_name] = line_value_list
    return pd_data


def calculate_arg_by_pd_col(data_list):
    '''
    通关pandas DataFrame的列计算平均值
    :param data_list: 含有多个pd对象的列表
    :return:
    '''
    data = dict()
    for item_pd in data_list:
        for col, row in item_pd.iteritems():
            data[col] = '%.2f' % item_pd[col].mean()
    return data
