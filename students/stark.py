from stark.service.stark import site, StarkConfig
from .models import *
from students.modelConfig.student import *
from students.modelConfig.Family import *


site.register(StudentInfo, StudentConfig)
site.register(HealthInfo)
site.register(FamilyInfo, FamilyInfoConfig)
site.register(StudentParents)
site.register(StudentToParents)
site.register(HealthInfo, SelfHealthInfoConfig, prev='self')
site.register(FamilyInfo, SelfFamilyInfoConfig, prev='self')
site.register(StudentToParents, SelfParentsInfoConfig, prev='self')
