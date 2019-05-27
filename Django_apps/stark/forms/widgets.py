from django import forms


class DateTimePickerInput(forms.TextInput):
    template_name = 'wigets/lay_time.html'


