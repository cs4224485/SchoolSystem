from rest_framework.viewsets import ViewSetMixin
from rest_framework.views import APIView, Response
from school.models import TableSettings, SchoolInfo, StuClass, Grade
from Django_apps.students.models import StudentInfo
from APIS.serialize.surver_form import SchoolSerializers, GradeSerializers, ClassSerializers, StudentSerializers
from utils.base_response import BaseResponse
from utils.common import order_by_class


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
            else:
                class_queryset = list(StuClass.objects.filter(grade=grade, school_id=school_id).all().distinct())
                class_queryset = order_by_class(class_queryset)
                class_se = ClassSerializers(class_queryset, many=True)
                res.data = {'_class': class_se.data}
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

        class_id = request.query_params.get('class_id')
        if not class_id:
            res.code = 403
            res.msg = "请提供班级ID"
            return Response(res.get_dict)

        student_list = StudentInfo.objects.filter(stu_class_id=class_id).values('full_name', 'id').distinct()
        student_se = StudentSerializers(student_list, many=True)
        res.data = {'students': student_se.data}
        return Response(res.get_dict)
