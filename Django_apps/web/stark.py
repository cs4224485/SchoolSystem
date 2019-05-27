from stark.service.stark import site
from Django_apps.web.views.survey_forms import TableSettingsConfig, DetailsOfFilling
from school.models import TableSettings, TableInfo
from Django_apps.web.views.student import StudentInfo, StudentConfig, SchoolStudentConfig
from Django_apps.web.views.teacher import TeacherInfoConfig, SchoolTeacherConfig
from teacher.models import TeacherInfo
from Django_apps.web.views.school import SchoolInfoConfig
from school.models import SchoolInfo
from stark.service.stark import site
from Django_apps.weixinApp.models import Emblem
from Django_apps.web.views.wechat_applet.emblem import EmblemHandler

site.register(Emblem, EmblemHandler)
site.register(TeacherInfo, stark_config=TeacherInfoConfig)
site.register(TeacherInfo, stark_config=SchoolTeacherConfig, prev='school')
site.register(SchoolInfo, SchoolInfoConfig)
# site.register(models.UserInfo, UserInfoConfig)
site.register(StudentInfo, StudentConfig)
site.register(StudentInfo, SchoolStudentConfig, prev='school')
site.register(TableSettings, TableSettingsConfig)
site.register(TableInfo, DetailsOfFilling)
