from rest_framework.views import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSetMixin
from APIS.serialize.mental_info import *
from utils.base_response import BaseResponse
from teacher import models as tea_models


class AppointmentInfoViewSet(ViewSetMixin, APIView):
    '''
    获取预约心理老师的相关信息，如 选择的学生，心理老师和可预约的时间
    '''

    def list(self, request, *args, **kwargs):
        message = BaseResponse()
        try:
            class_id = request.GET.get('class_id', '16')
            stu_class = sch_models.StuClass.objects.filter(id=class_id).first()
            student_queryset = stu_models.StudentInfo.objects.filter(stu_class=stu_class)
            teacher_queryset = tea_models.TeacherInfo.objects.filter(identity=2)
            stu_se = StudentListSerialize(student_queryset, many=True)
            teacher_se = PsychologyTeacherSerialize(teacher_queryset, many=True)
            message.state = True
            message.data = {'student': stu_se.data, 'teacher': teacher_se.data}
        except Exception as e:
            message.msg = '获取失败'
        return Response(message.get_dict)


class GetPerClassStudent(ViewSetMixin, APIView):
    '''
    根据老师获取每个班级的学生和班级名称，班主任只获取所负责的班级，心理老师获取全部的班级
    '''

    def list(self, request, *args, **kwargs):
        message = BaseResponse()
        try:
            teacher_id = request.GET.get('teacher_id', '11')
            teacher_info = tea_models.TeacherInfo.objects.filter(id=teacher_id).values('identity__title', 'school',
                                                                                       'teachers__stu_class__grade',
                                                                                       'teachers__stu_class').first()
            grade = teacher_info.get('teachers__stu_class__grade')
            if teacher_info.get('identity__title') != '心理老师':
                stu_class = sch_models.StuClass.objects.filter(grade=grade, id=teacher_info.get('teachers__stu_class'),
                                                               school=teacher_info.get('school'))
            else:
                stu_class = sch_models.StuClass.objects.filter(school=teacher_info.get('school'))
            data_list = []
            for item in stu_class:
                class_name = '%s%s' % (item.grade.get_grade_name_display(), item.name)
                student_queryset = stu_models.StudentInfo.objects.filter(stu_class=item, school=teacher_info.get('school')).values('id', 'full_name')
                if student_queryset:
                    student_dict = {class_name: []}
                    for student in student_queryset:
                        student_dict[class_name].append(student)
                    data_list.append(student_dict)
            message.state = True
            message.data = data_list
        except Exception as e:
            message.msg = '获取学生列表失败'
        return Response(message.__dict__)
