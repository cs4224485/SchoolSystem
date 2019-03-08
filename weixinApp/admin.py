from django.contrib import admin
from weixinApp import models

admin.site.register(models.WechatUserInfo)
admin.site.register(models.Emblem)
admin.site.register(models.EmblemType)