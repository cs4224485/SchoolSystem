from stark.service.stark import StarkConfig
from web.forms.wechat_app.emblem import EmblemForm


class EmblemHandler(StarkConfig):
    '''
    徽章后台管理
    '''
    list_display = ['emblem_name', 'description']

    model_form_class = EmblemForm

