from django.db import models

# Create your models here.


class TeacherInfo(models.Model):
    last_name = models.CharField(verbose_name='老师姓', max_length=128)
    first_name = models.CharField(verbose_name='老师名', max_length=128)
    gender_choice = ((1, '男'), (2, '女'))
    gender = models.IntegerField(choices=gender_choice, verbose_name='性别', null=True, blank=True)
    birthday = models.DateField(verbose_name='老师生日', null=True, blank=True)
    telephone = models.CharField(verbose_name='电话号码', max_length=32, null=True, blank=True)
    wechat = models.CharField(verbose_name='微信', max_length=32, null=True, blank=True)
    wechat_open_id = models.ForeignKey(verbose_name='openID', to='students.WechatOpenID', null=True, on_delete=models.CASCADE, blank=True, related_name='teacher_open_id')
    course = models.ManyToManyField(to='Course', verbose_name='老师所带科目', null=True, blank=True)
    identity = models.ForeignKey(to='Identity', verbose_name='老师的身份', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(to='school.SchoolInfo', verbose_name='老师所在学校', on_delete=models.CASCADE)

    def __str__(self):
        return self.last_name + self.first_name


class Course(models.Model):
    title = models.CharField(verbose_name='科目名称', max_length=32)

    def __str__(self):
        return self.title


class Identity(models.Model):
    title = models.CharField(verbose_name='身份', max_length=32)

    def __str__(self):
        return self.title


class ClassToTeacher(models.Model):
    stu_class = models.ForeignKey(to="school.StuClass", verbose_name='班级', on_delete=models.CASCADE, related_name='handle_class', limit_choices_to={"school_id__in": ['115']})
    teacher = models.ForeignKey(to='TeacherInfo', verbose_name='老师', on_delete=models.CharField, related_name="teachers")
    create_date = models.DateField(verbose_name='创建时间', auto_now=True)