'''
通用接口
'''
from rest_framework.views import Response
from rest_framework.views import APIView
from school.models import SchoolInfo
from APIS.serialize.common import SchoolSerializers, GradeSerializers, ClassSerializers
from utils.base_response import BaseResponse
from utils.common import order_by_class
from school.models import SchoolInfo, StuClass, Grade


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
