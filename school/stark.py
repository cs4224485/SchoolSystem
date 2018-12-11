from stark.service.stark import site, StarkConfig
from .models import *
from school.modelConfig.school import *


site.register(SchoolInfo, SchoolInfoConfig)
site.register(ChoiceField, ChoiceFieldConfig)
site.register(FieldType)
site.register(TableSettings, SchoolSettingsConfig)
site.register(SettingToField, SettingToFieldConfig)
site.register(StuClass)
site.register(Grade)
