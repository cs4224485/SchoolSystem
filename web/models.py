from django.db import models
from rbac.models import UserInfo as RbacUserInfo
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


# Create your models here.


class UserInfo(RbacUserInfo):
    """
    内部员工表
    """
    nickname = models.CharField(verbose_name='姓名', max_length=16)
    phone = models.CharField(verbose_name='手机号', max_length=32)

    gender_choices = (
        (1, '男'),
        (2, '女'),
    )
    gender = models.IntegerField(verbose_name='性别', choices=gender_choices, default=1)

    def __str__(self):
        return self.nickname

    class Meta:
        db_table = 'UserInfo'



