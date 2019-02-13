from django.db import models
from django.contrib.contenttypes.fields import GenericRelation
# Create your models here


class TeacherInfo(models.Model):
    last_name = models.CharField(verbose_name='老师姓', max_length=128)
    first_name = models.CharField(verbose_name='老师名', max_length=128)
    gender_choice = [(1, '男'), (2, '女')]
    gender = models.SmallIntegerField(choices=gender_choice, verbose_name='性别', default=None, blank=True, null=True)
    birthday = models.DateField(verbose_name='老师生日', null=True, blank=True)
    telephone = models.CharField(verbose_name='电话号码', unique=True, max_length=32, null=True, blank=True)
    wechat = models.CharField(verbose_name='微信',  max_length=32, null=True, blank=True)
    course = models.ManyToManyField(to='school.Course', verbose_name='老师所带科目', null=True, blank=True)
    identity = models.ForeignKey(to='Identity', verbose_name='老师的身份', on_delete=models.CASCADE, null=True)
    school = models.ForeignKey(to='school.SchoolInfo', verbose_name='老师所在学校', on_delete=models.CASCADE)
    wx_info = GenericRelation(to='weixinApp.WechatUserInfo')

    def __str__(self):
        return self.last_name + self.first_name

    class Meta:
        unique_together = (("first_name", "last_name", 'birthday', 'telephone', 'wechat'),)


class Identity(models.Model):
    title = models.CharField(verbose_name='身份', max_length=32)

    def __str__(self):
        return self.title


class ClassToTeacher(models.Model):
    '''
    教师与班级映射
    '''
    stu_class = models.ForeignKey(to="school.StuClass", verbose_name='班级', on_delete=models.CASCADE, related_name='handle_class')
    teacher = models.ForeignKey(to='TeacherInfo', verbose_name='老师', on_delete=models.CharField, related_name="teachers")
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now=True)
    relate_choice = ((1, '班主任'), (2, '代课老师'))
    relate = models.SmallIntegerField(verbose_name='教师与班级的对应关系', choices=relate_choice, default=1)

    def __str__(self):
        return "关联老师:%s 班级: %s" % (self.teacher.last_name+self.teacher.first_name, self.stu_class.name)

