from stark.service.stark import site, StarkConfig
from .models import *
from teacher.modelconfig.teacher_info import TeacherInfoConfig

site.register(TeacherInfo, stark_config=TeacherInfoConfig)
