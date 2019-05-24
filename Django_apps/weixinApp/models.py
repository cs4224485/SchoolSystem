from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class WechatUserInfo(models.Model):
    '''
    微信用户信息
    '''

    nickname = models.CharField(verbose_name='微信昵称', max_length=64, db_index=True)
    avatar = models.URLField(verbose_name='头像', max_length=128)
    updated_time = models.DateField(verbose_name="更新时间", null=True, blank=True)
    create_time = models.DateField(verbose_name='创建时间', auto_now=True)
    user_type_choice = ((1, '家长'), (2, '老师'), (3, '学生'))
    user_type = models.SmallIntegerField(verbose_name='用户类型', choices=user_type_choice)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    bind_info = models.OneToOneField(verbose_name='绑定openid的信息', to='WechatBindInfo', on_delete=models.CASCADE,
                                     related_name='wx_user')

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'WechatUserInfo'


class WechatBindInfo(models.Model):
    '''
    微信绑定信息
    '''

    school = models.ForeignKey(verbose_name='学校ID', to='school.SchoolInfo', on_delete=models.CASCADE)
    open_id = models.CharField(verbose_name='openid', max_length=128)
    salt = models.CharField(verbose_name='用于加密', max_length=32, )
    status_choice = ((1, '正常'), (2, '异常'))
    status = models.SmallIntegerField(verbose_name='账号状态', choices=status_choice, default=1)
    bind_time = models.DateField(verbose_name='绑定小程序的事件', auto_now=True)

    class Meta:
        unique_together = (('school', 'open_id'),)
        db_table = 'WechatBindInfo'


class Schedule(models.Model):
    '''
    微信用户每日日程信息
    '''

    time = models.TimeField(verbose_name='时间')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    event_choice = ((1, '家访'), (2, '预约'))
    event = models.PositiveSmallIntegerField(verbose_name='事件类型', choices=event_choice)
    create_time = models.DateField(verbose_name='创建时间', auto_now=True)
    date = models.DateField(verbose_name='日期时间')

    class Meta:
        db_table = 'Schedule'


class IndexNotification(models.Model):
    '''
    小程序日常页面相关的消息
    '''

    create_time = models.DateTimeField(auto_now=True, verbose_name='创建时间')
    event_choice = ((1, '家访'), (2, '徽章'), (3, '报表'), (4, '作业'))
    event = models.PositiveSmallIntegerField(verbose_name='事件类型', choices=event_choice)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    associated_users = models.ManyToManyField(verbose_name='关联的用户', to='WechatUserInfo')
    is_display = models.BooleanField(verbose_name='是否在前端展示', default=True)

    class Meta:
        db_table = 'IndexNotification'


# ######### 家访相关 ############
class FamilyVisitRecord(models.Model):
    '''
    家访记录
    '''

    student = models.ForeignKey(to="students.StudentInfo", verbose_name='对应学生', on_delete=models.CASCADE)
    teacher = models.ForeignKey(to="teacher.TeacherInfo", verbose_name='访问的老师', on_delete=models.CASCADE)
    reason = models.TextField(verbose_name='访问原因', max_length=150)
    relate_parents = models.ManyToManyField(to='WechatUserInfo', verbose_name='关联家长的微信信息')
    state_choice = ((1, '预约中'), (2, '已完成'), (3, '已取消'))
    state = models.SmallIntegerField(choices=state_choice, verbose_name='预约状态', default=1)
    schedule = GenericRelation(to='Schedule')
    notification = GenericRelation(to='IndexNotification')

    class Meta:
        db_table = 'FamilyVisitRecord'


# ######## 徽章系统相关 ###############
class EmblemType(models.Model):
    '''
    徽章类型描述
    '''
    title = models.CharField(verbose_name='标题描述', max_length=64)
    pid = models.ForeignKey(verbose_name='父级分类', to='EmblemType', on_delete=models.CASCADE, null=True,
                            blank=True, related_name='parents', help_text='如果不为空代表是一个描述子类')

    class Meta:
        db_table = 'EmblemType'

    def __str__(self):
        return self.title


class Emblem(models.Model):
    '''
    徽章表
    '''
    emblem_name = models.CharField(verbose_name='徽章名称', max_length=64)
    custom_name = models.CharField(verbose_name='自定义名称', max_length=64, null=True, blank=True)
    icon = models.FileField(upload_to='emblem/icon', verbose_name='徽章图标')
    photo = models.FileField(upload_to='emblem/photo', verbose_name='自定制图片', null=True, blank=True)
    description = models.TextField(verbose_name='徽章描述', max_length=128)
    is_custom = models.BooleanField(verbose_name='是否允许自定制', default=False)
    school = models.ForeignKey(to='school.SchoolInfo', verbose_name='学校', on_delete=models.CASCADE,
                               help_text='如果允许自定制，关联学校的ID', null=True, blank=True, default=None)
    classification_choice = ((1, '鼓励与表扬'), (2, '惩罚与批评'))
    classification = models.SmallIntegerField(choices=classification_choice, verbose_name='徽章分类选择')
    issuer_choice = ((1, '老师'), (2, '家长'), (3, '两者皆可'))
    issuer = models.SmallIntegerField(choices=issuer_choice, verbose_name='颁发者分类')
    # 徽章维度信息
    scope_choice = ((1, '校级'), (2, '班级'))
    scope = models.SmallIntegerField(choices=scope_choice, verbose_name='颁发范围', null=True, blank=True, default=None)
    grade = models.ManyToManyField(to='school.Grade', verbose_name='适用年级', null=True, blank=True)
    subject = models.ManyToManyField(to='school.Course', verbose_name='学科维度', null=True, blank=True)
    emblem_type = models.ForeignKey(to='EmblemType', on_delete=models.CASCADE, verbose_name='徽章类型')

    class Meta:
        db_table = 'Emblem'
        unique_together = (('emblem_name', 'emblem_type'),)

    def __str__(self):
        return self.emblem_name


class IssuedRecord(models.Model):
    '''
    徽章颁发记录
    '''

    emblem = models.ForeignKey(verbose_name='徽章', to='Emblem', on_delete=models.CASCADE)
    issuing_person = models.ForeignKey(verbose_name='颁发人', to='WechatUserInfo', on_delete=models.CASCADE)
    student = models.ManyToManyField(verbose_name='对应学生', to='students.StudentInfo')
    date = models.DateField(verbose_name='颁发日期', auto_now=True)
    time = models.TimeField(verbose_name='颁发时间', auto_now=True)
    comment = models.TextField(verbose_name='评语', max_length=128)
    notification = GenericRelation(to='IndexNotification')

    class Meta:
        db_table = 'IssuedRecord'
