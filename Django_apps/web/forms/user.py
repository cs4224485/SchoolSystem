from django import forms
from stark.service.stark import StarkModelForm, StarkForm
from django.core.exceptions import ValidationError
from Django_apps.web import models
from utils.common import gen_md5_password


class ResetPasswordForm(StarkForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5_password(password)
        return self.cleaned_data


class UserInfoAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email',  'roles']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5_password(password)
        return self.cleaned_data


class UserInfoChangeModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email',  'roles']