from django.contrib import admin
from school import models
# Register your models here.
admin.site.register(models.TableSettings)
admin.site.register(models.ChoiceField)
admin.site.register(models.FieldType)
admin.site.register(models.ScopeOfFilling)
admin.site.register(models.StuClass)