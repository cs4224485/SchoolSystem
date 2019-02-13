from rest_framework.views import APIView, Response
from utils.base_response import BaseResponse
from teacher import models as tea_model


class TeacherToCourseInfoViewSet(APIView):
    '''
    根据教师获取该教师所教授的课程
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            course_id = request.GET.get('courseId')
            class_id = request.GET.get('classId')
            teacher_obj = tea_model.TeacherInfo.objects.filter(course=course_id,
                                                               teachers__stu_class=class_id).values('id', 'last_name',
                                                                                                    'first_name').first()
            if not teacher_obj:
                res.msg = "未能查询到代课老师"
                res.code = -1
                return Response(res.get_dict)
            res.data = teacher_obj
            res.code = 200
        except Exception as e:
            res.code = -1
            res.msg = '获取代课老师信息失败'
        return Response(res.get_dict)
