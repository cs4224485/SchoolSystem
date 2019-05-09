from stark.service.stark import site
from web import models
from web.modelConfig.user import UserInfoConfig
from web.views.survey_forms import TableSettingsConfig, DetailsOfFilling
from school.models import TableSettings, TableInfo

# site.register(models.UserInfo, UserInfoConfig)

site.register(TableSettings, TableSettingsConfig)
site.register(TableInfo, DetailsOfFilling)
