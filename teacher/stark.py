from stark.service.stark import site, StarkConfig
from .models import *
from teacher.modelconfig.teacher_info import TeacherInfoConfig
from teacher.modelconfig.every_school_teacher import SchoolTeacherConfig

site.register(TeacherInfo, stark_config=TeacherInfoConfig)
site.register(TeacherInfo, stark_config=SchoolTeacherConfig, prev='school')
