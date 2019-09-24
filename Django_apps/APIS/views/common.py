'''
通用接口
'''
from rest_framework.views import Response
from rest_framework.views import APIView
from APIS.serialize.common import SchoolSerializers, GradeSerializers, ClassSerializers, StudentSerializers, \
    StudentDetailSerializes, CourseSerializes
from utils.base_response import BaseResponse
from utils.common import order_by_class
from school.models import SchoolInfo, StuClass, Grade, Course
from Django_apps.students.models import StudentInfo, FamilyInfo, HomeAddress


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
        if not student_id:
            res.code = 403
            res.msg = '请提供学生ID'
            return Response(res.get_dict)
        print(student_id)
        home_obj = HomeAddress.objects.filter(family__student_id=student_id).first()
        print(home_obj)