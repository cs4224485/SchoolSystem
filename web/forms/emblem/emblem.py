from django import forms
from weixinApp.models import Emblem


class EmblemForm(forms.ModelForm):

    class Meta:
        model = Emblem
        fields = "__all__"