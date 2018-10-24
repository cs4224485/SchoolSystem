from stark.service.stark import StarkConfig
from django import forms


class FamilyInfoConfig(StarkConfig):
    list_display = [ 'student', 'family_status', 'living_type', 'language',]

    def get_model_form_class(self):
        class ModelForm(forms.ModelForm):
            class Meta:
                model = self.model_class
                exclude = ('member_of_family', )
        return ModelForm