from stark.service.stark import site
from weixinApp.models import Emblem
from web.views.wechat_applet.emblem import EmblemHandler

site.register(Emblem, EmblemHandler)
