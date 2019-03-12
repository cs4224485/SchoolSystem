from django import forms
from weixinApp.models import Emblem


class EmblemForm(forms.ModelForm):
    class Meta:
        model = Emblem
        fields = ('emblem_name', 'icon', 'description', 'classification',
                  'issuer', 'scope', 'emblem_type', 'grade', 'subject')

