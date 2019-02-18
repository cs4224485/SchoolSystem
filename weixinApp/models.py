from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
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
    bind_info = models.OneToOneField(verbose_name='绑定openid的信息', to='WechatBindInfo', on_delete=models.CASCADE, related_name='wx_user')

    def __str__(self):
        return self.nickname


class WechatBindInfo(models.Model):
    '''
    微信绑定信息
    '''

    school = models.ForeignKey(verbose_name='学校ID', to='school.SchoolInfo', on_delete=models.CASCADE)
    open_id = models.CharField(verbose_name='openid', max_length=128)
    salt = models.CharField(verbose_name='用于加密', max_length=32, )
    status_choice = ((1, '正常'), (2, '异常'))
    status = models.SmallIntegerField(verbose_name='账号状态', choices=status_choice, default=1)

    class Meta:
        unique_together = (('school', 'open_id'),)


