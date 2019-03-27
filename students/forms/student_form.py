from django import forms
from django.forms import fields as Ffields
from django.forms import widgets as Fwidgets
from students import models as stumodels


class StudentEditForm(forms.ModelForm):
    gender = Ffields.ChoiceField(required=True, choices=((1, '男'), (2, '女')), widget=Fwidgets.RadioSelect())
    birthday = Ffields.DateField(required=False, widget=Fwidgets.DateInput(
        attrs={'class': 'form-control', 'type': 'date', 'style': 'width: 600px'}))

    class Meta:
        model = stumodels.StudentInfo
        fields = ("last_name", 'first_name', 'full_name', "gender", "birthday", 'period', 'school', 'period',
                  'age', 'day_age', 'constellation', 'chinese_zodiac', 'school')
        widgets = {
            "last_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "first_name": Fwidgets.TextInput(attrs={'class': 'form-control', 'style': 'width: 600px'}),
            "school": Ffields.Select(attrs={'class': 'form-control', 'style': 'width: 600px'})
        }
