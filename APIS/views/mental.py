from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from school import models as sch_models
from students import models as stu_models
from APIS.serialize.mental_info import *


class AppointmentInfoViewSet(ViewSetMixin, APIView):
    '''
    获取预约心理老师的相关信息，如 选择的学生，心理老师和可预约的时间
    '''
    def list(self, request, *args, **kwargs):
        message = {
            'state': False,
            'msg': '',
            'data': []
        }
        try:
            class_id = request.GET.get('class_id', '16')
            print(class_id)
            stu_class = sch_models.StuClass.objects.filter(id=class_id).first()
            student_queryset = stu_models.StudentInfo.objects.filter(stu_class=stu_class)
            teacher_queryset = tea_models.TeacherInfo.objects.filter(identity=2)
            stu_se = StudentListSerialize(student_queryset, many=True)
            teacher_se = PsychologyTeacherSerialize(teacher_queryset, many=True)
            message['state'] = True
            message['data'] = {'student': stu_se.data, 'teacher': teacher_se.data}
        except Exception as e:
            message['msg'] = '获取失败'
        return Response(message)
