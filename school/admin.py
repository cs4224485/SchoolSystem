from django.contrib import admin
from school import models
# Register your models here.
admin.site.register(models.SchoolSettings)
admin.site.register(models.ScopeOfFilling)
admin.site.register(models.StuClass)