from django.contrib import admin
from teacher import models
# Register your models here.
admin.site.register(models.TeacherInfo)
admin.site.register(models.Identity)
admin.site.register(models.ClassToTeacher)
