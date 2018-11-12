from django import template
from school import models

register = template.Library()


@register.inclusion_tag('setting/fields.html')
def fields():
    stu_info_choice = models.ChoiceField.objects.filter(field_type=1)
    hel_info_choice = models.ChoiceField.objects.filter(field_type=2)
    fam_info_choice = models.ChoiceField.objects.filter(field_type=3)
    par_info_choice = models.ChoiceField.objects.filter(field_type=4)
    customization_field = models.ChoiceField.objects.filter(field_type=5)
    return {'stu_info_choice': stu_info_choice,
            'hel_info_choice': hel_info_choice,
            'fam_info_choice': fam_info_choice,
            'par_info_choice': par_info_choice,
            'customization_field': customization_field,
            }


