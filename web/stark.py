from stark.service.stark import site
from web import models
from web.modelConfig.user import UserInfoConfig

site.register(models.UserInfo, UserInfoConfig)
