from django import forms
from weixinApp.models import Emblem, EmblemType
from stark.service.stark import StarkModelForm
from django.forms import widgets
from django.forms import fields
from school.models import Course, Grade


class EmblemForm(StarkModelForm):
    issuer = fields.ChoiceField(widget=widgets.RadioSelect(), label='颁发者',
                                choices=((1, '老师'), (2, '家长'), (3, '两者皆可')))

    classification = fields.ChoiceField(widget=widgets.RadioSelect(), label='徽章分类',
                                        choices=((1, '鼓励与表扬'), (2, '惩罚与批评')))
    scope = fields.ChoiceField(required=False, widget=widgets.RadioSelect(), label='颁发范围',
                               choices=((1, '校级别'), (2, '班级')))
    subject = forms.ModelMultipleChoiceField(required=False, label='关联课程', queryset=Course.objects.all(),
                                             widget=widgets.CheckboxSelectMultiple())
    grade = forms.ModelMultipleChoiceField(required=False, label='关联年级', queryset=Grade.objects.all(),
                                           widget=widgets.CheckboxSelectMultiple())
    icon = fields.FileField(widget=fields.FileInput(attrs={'style': 'display:none'}), label='徽章图片')

    emblem_type = forms.ModelChoiceField(required=False, label='徽章类型',
                                         queryset=EmblemType.objects.exclude(id__in=[item.pid.id for item in
                                                                                     EmblemType.objects.filter(
                                                                                         pid__isnull=False)]))
    is_custom = fields.ChoiceField(widget=widgets.RadioSelect(), label='是否允许自定制',
                                   choices=((True, '允许'), (False, '禁止')), initial=False)

    class Meta:
        model = Emblem
        fields = ('emblem_name', 'icon', 'description', 'classification', 'scope', 'is_custom',
                  'issuer', 'subject', 'emblem_type', 'grade',)
