from web import models
from stark.service.stark import StarkConfig
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from django.urls import re_path
from web.forms.user import ResetPasswordForm, UserInfoAddModelForm, UserInfoChangeModelForm


class UserInfoConfig(StarkConfig):
    def display_reset_pwd(self, row=None, header=None):
        if header:
            return '重置密码'
        reset_url = self.reverse_commons_url(self.get_url_name('reset_pwd'), pk=row.pk)
        return mark_safe("<a href='%s'>重置密码</a>" % reset_url)

    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = models.UserInfo.objects.filter(id=pk).first()
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'stark/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def get_model_form_class(self, is_add=False):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    def extra_urls(self):
        patterns = [
            re_path(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                    name=self.get_url_name('reset_pwd')),
        ]
        return patterns

    list_display = ['nickname', 'gender', 'phone', 'email', display_reset_pwd]
