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
            teacher_id = request.GET.get('teacherId')
            teacher_obj = tea_model.TeacherInfo.objects.filter(id=teacher_id).first()

            if not teacher_obj:
                res.msg = "该教师不存在"
                return Response(res.get_dict)

            course_queryset = teacher_obj.course.all()
            res.data = []
            for course_item in course_queryset:
                course_dict = {
                    'course_id': course_item.id,
                    'course_des': course_item.course_des
                }
                res.data.append(course_dict)
            res.code = 200
        except Exception as e:
            res.code = 500
            res.msg = '获取课程信息失败'
        return Response(res.get_dict)
