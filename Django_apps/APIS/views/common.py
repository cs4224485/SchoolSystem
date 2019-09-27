'''
通用接口
'''
from rest_framework.views import Response
from rest_framework.views import APIView
from APIS.serialize.common import SchoolSerializers, GradeSerializers, ClassSerializers, StudentSerializers, \
    StudentDetailSerializes, CourseSerializes, StudentHomeSerializes, StudentParentSerializes, StudentListSerializes
from utils.base_response import BaseResponse
from utils.common import order_by_class
from school.models import SchoolInfo, StuClass, Grade, Course
from Django_apps.students.models import StudentInfo, FamilyInfo, HomeAddress, StudentToParents, ScaleQuestion, \
    ChoiceQuestion


class GetAllSchoolViewSet(APIView):
    '''
    获取所有的学校
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            school_queryset = SchoolInfo.objects.all()
            school_se = SchoolSerializers(school_queryset, many=True)
            res.code = 200
            res.data = {'school': school_se.data}
        except Exception as e:
            res.code = 500
            res.msg = '获取失败'
        return Response(res.get_dict)


class SchoolInfoViewSet(APIView):
    '''
    根据学校ID获取某一学校数据
    '''

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


class FilterGradeAndClassViewSet(APIView):
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
    获取每个班级学生列表
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


class StudentDetailInfo(APIView):
    '''
    获取学生详细信息
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
            if not student_obj:
                res.code = 404
                res.msg = "未查找到该学生"
                return Response(res.get_dict)
            student_se = StudentDetailSerializes(student_obj)
            res.data = {'student': student_se.data}
            res.code = 200
        except Exception as e:
            print(e)
            res.code = 500
            res.msg = '获取失败'
        return Response(res.get_dict)


class CourseViewSet(APIView):
    '''
    获取课程信息
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            course_queryset = Course.objects.all()
            course_se = CourseSerializes(course_queryset, many=True)
            res.code = 200
            res.msg = "获取成功"
            res.data = course_se.data
        except Exception as e:
            print(e)
            res.code = 500
            res.msg = "获取失败"
        return Response(res.get_dict)


class StudentHomeAddressViewSet(APIView):
    '''
    获取家庭地址
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        student_id = request.query_params.get('student_id')
        try:
            if not student_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)

            home_obj = HomeAddress.objects.filter(family__student_id=student_id).first()
            se = StudentHomeSerializes(home_obj).data
            res.data = se
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = "获取失败"
        return Response(res.get_dict)


class ParentInfoViewSet(APIView):
    '''
    学生父母信息
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        student_id = request.query_params.get('student_id')
        try:
            if not student_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)

            parent_queryset = StudentToParents.objects.filter(student_id=student_id)
            se = StudentParentSerializes(parent_queryset, many=True)
            res.data = se.data
            res.code = 200

        except Exception as e:
            res.code = 500
            res.msg = "获取失败"

        return Response(res.get_dict)


class FormInfoViewSet(APIView):
    '''
    表单信息
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        student_id = request.query_params.get('student_id')
        try:
            if not student_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)

            data_list = []
            # 获取填写矩阵量表相关信息
            sc_query = ScaleQuestion.objects.filter(student_id=student_id)
            for item in sc_query:
                scale_title = item.scale.title
                option_val = []
                data_dict = {scale_title: {'options': [], 'line': []}}
                for val in item.scale_value.all():
                    data_dict[scale_title]['line'].append({val.title.des: val.value.des})
                    option_val.append(val.value.des)
                for options in item.scale.options.all():
                    data_dict[scale_title]['options'].append(options.des)
                data_list.append(data_dict)
            res.code = 200
            res.data = data_list
        except Exception as e:
            res.code = 500
            res.msg = "获取失败"

        return Response(res.get_dict)


class ChoiceInfoViewSet(APIView):
    '''
    选择题信息
    '''
    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        student_id = request.query_params.get('student_id')
        try:
            if not student_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)
            data_list = []
            choice_query = ChoiceQuestion.objects.filter(student_id=student_id)
            for item in choice_query:
                title = item.choice_table.title
                data_dict = {title: {'options': [], 'selected': []}}
                for op in item.choice_table.opdes.all():
                    data_dict[title]['options'].append(op.des)
                for val in item.values.all():
                    data_dict[title]['selected'].append(val.des)
                data_list.append(data_dict)
            res.code = 200
            res.data = data_list
        except Exception as e:
            res.code = 500
            res.msg = "获取失败"
        return Response(res.get_dict)


class StudentListViewSet(APIView):
    '''
    学生列表
    '''
    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        school_id = request.query_params.get('school_id')
        try:
            if not school_id:
                res.code = 403
                res.msg = '请提供学生ID'
                return Response(res.get_dict)
            student_queryset = StudentInfo.objects.filter(school_id=school_id).order_by("grade", "stu_class").all()
            student_se = StudentListSerializes(student_queryset, many=True).data

            res.data = student_se
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = "获取失败"
        return Response(res.get_dict)

