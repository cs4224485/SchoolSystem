# Author: harry.cai
# DATE: 2019/1/1
from django import forms
from django.forms.widgets import *
from rbac import models


class RoleModelForm(forms.ModelForm):
    class Meta:
        model = models.Role
        fields = ['title', ]
        widgets = {
            'title': TextInput(attrs={'class': 'form-control'})
        }
