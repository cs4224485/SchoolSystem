from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Country)
admin.site.register(StudentInfo)
admin.site.register(Allergy)
admin.site.register(InheritedDisease)

admin.site.register(GraduateInstitutions)
admin.site.register(FamilyStatus)
admin.site.register(FamilyInfo)
admin.site.register(StudentParents)
admin.site.register(StudentToParents)
admin.site.register(ScaleQuestion)
admin.site.register(ChoiceQuestion)







