from stark.service.stark import site, StarkConfig
from .models import *
from students.modelConfig.student import *
from students.modelConfig.every_school_student import SchoolStudentConfig

site.register(StudentInfo, StudentConfig)
site.register(StudentInfo, SchoolStudentConfig, prev='school')
