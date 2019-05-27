from stark.service.stark import StarkConfig
from Django_apps.web.forms.wechat_app.emblem import EmblemForm


class EmblemHandler(StarkConfig):
    '''
    徽章后台管理
    '''
    list_display = ['emblem_name', 'description']

    model_form_class = EmblemForm

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        '''
        编辑徽章
        :param request:
        :param pk:
        :param template:
        :param args:
        :param kwargs:
        :return:
        '''
        return super().change_view(request, pk, template='emblem/emblem_change.html', *args, **kwargs)

    def add_view(self, request, template='stark/change.html', *args, **kwargs):
        '''
        添加徽章
        :param request:
        :param template:
        :param args:
        :param kwargs:
        :return:
        '''
        return super().add_view(request, template='emblem/emblem_change.html', *args, **kwargs)

    def get_form(self, model_form, request, modify=False, *args, **kwargs):
        form = model_form(request.POST, request.FILES)
        if modify:
            obj = kwargs.get('obj')
            form = model_form(request.POST, request.FILES, instance=obj)
        return form
