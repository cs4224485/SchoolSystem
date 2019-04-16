from stark.service.stark import site
from web import models
from web.modelConfig.user import UserInfoConfig
from web.views.survey_forms import TableSettingsConfig
from school.models import TableSettings
# site.register(models.UserInfo, UserInfoConfig)

site.register(TableSettings, TableSettingsConfig)