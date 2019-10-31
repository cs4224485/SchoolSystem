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


class PerformanceRecord(models.Model):
    student = models.ForeignKey(to='students.StudentInfo', verbose_name='对应学生', on_delete=models.CASCADE,
                                related_name='stu_performance')
    option_choice = ((1, '与年龄明显不符的集中困难'), (2, '不能遵守课堂与学校的规则，如擅自离座、走动'), (3, '行为冲动，如爱插嘴、攻击他人'),
                     (4, '尖叫'), (5, '情绪失控'), (6, '与人缺乏眼神交流'), (7, '动作刻板，环境刻板'), (8, "攻击他人"), (9, "敌意"), (10, "愤怒情绪"),
                     (11, "拒绝身体接触"), (12, "手脚配合笨拙，易跌倒"), (13, "东西整理乱"), (14, "阅读时必须手指指读读，容易漏字、漏行"),
                     (15, "b/d,p/q,w/m这类字母无法区分"), (16, "手指精细动作有困难")
                     )
    options = models.SmallIntegerField(choices=option_choice, verbose_name="选项")
    create_time = models.DateTimeField(auto_now=True, verbose_name="创建时间")
