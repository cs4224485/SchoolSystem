from django.db import models


# Create your models here.


class IndividualStudentRecord(models.Model):
    '''
    特殊学生教育档案记录表
    '''
    student = models.ForeignKey(to='students.StudentInfo', verbose_name='对应学生', on_delete=models.CASCADE)
    scale_table = models.ForeignKey(to='students.ScaleQuestion', verbose_name='对相应的学生量表', on_delete=models.CASCADE)
    record_time = models.DateField(verbose_name='记录时间', auto_now=True)
    teacher = models.ForeignKey(to='teacher.TeacherInfo', verbose_name='记录的老师', on_delete=models.CASCADE)

    def __str__(self):
        return self.student.full_name


class Appointment(models.Model):
    '''
    预约心理老师
    '''
    student = models.ForeignKey(to='students.StudentInfo', verbose_name='对应学生', on_delete=models.CASCADE)
    teacher = models.ForeignKey(to='teacher.TeacherInfo', verbose_name='对应的心理老师', on_delete=models.CASCADE,
                                limit_choices_to={"id__in": [2]})
    time = models.DateField()

    class Meta:
        unique_together = (
            ('student', 'teacher', 'time')
        )


class AppointmentManage(models.Model):
    '''
    心理老师预约管理
    '''

    teacher = models.ForeignKey(to='teacher.TeacherInfo', verbose_name='对应的心理老师', on_delete=models.CASCADE,
                                limit_choices_to={"id__in": [2]})
    date = models.DateField(verbose_name='日期')
    student = models.ForeignKey(to='students.StudentInfo', verbose_name='对应学生', on_delete=models.CASCADE,
                                related_name='stu_appointment')
    time = models.ForeignKey(to='AvailableTime', verbose_name='对应时段', on_delete=models.CASCADE)


class AvailableTime(models.Model):
    '''
    可预约的时段
    '''
    time_choice = ((1, 'AM 9:00 - AM 10:00'), (2, 'PM15:30 - PM16:30'))
    time = models.IntegerField(choices=time_choice)


class TeacherEditTime(models.Model):
    '''
    心理老师编辑自己可预约的时间段
    '''

    teacher = models.ForeignKey(to='teacher.TeacherInfo', verbose_name='对应的心理老师', on_delete=models.CASCADE,
                                limit_choices_to={"id__in": [2]})
