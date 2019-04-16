import json
import os
from django.shortcuts import render
from stark.service.stark import StarkConfig
from django.urls import re_path
from django.utils.safestring import mark_safe
from school import models
from school.utils.common_utils import *
from django.http import JsonResponse
from web.service.survey_form_service import SurveyFormService


class TableSettingsConfig(StarkConfig):

    def get_add_btn(self):
        return mark_safe('<a href="%s" class="btn btn-success">添加</a>' % "/stark/school/tablesettings/settings/")

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)
        return val

    def get_urls(self):

        urlpatterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^settings/$', self.wrapper(self.form_crate), name='table_setting'),
            re_path(r'^(?P<pk>\d+)/setting_edit/$', self.wrapper(self.form_edit), name='edit_setting'),
            re_path(r'^(?P<pk>\d+)/release/$', self.wrapper(self.release), name='release'),
            re_path(r'^preview/$', self.wrapper(self.preview), name='preview'),
            re_path(r'^(?P<pk>\d+)/del/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())

        return urlpatterns

    def display_release(self, row=None, header=None):
        if header:
            return '设置'
        url = '/stark/school/tablesettings/%s/release/' % row.pk
        tag = '<a href="%s">设置</a>' % url
        return mark_safe(tag)

    def display_edit(self, row=None, header=False, *args, **kwargs):
        if header:
            return "编辑"
        url = '/stark/school/tablesettings/%s/setting_edit/' % row.pk
        return mark_safe(
            '<a href="%s"><i class="fa fa-edit" aria-hidden="true"></i></a></a>' % url)

    def display_count(self, row=None, header=False):
        if header:
            return '填表人数'
        return row.table_info.all().count()

    def form_crate(self, request):
        '''
        表单设置页面
        :param request:
        :return:
        '''
        school_list = models.SchoolInfo.objects.all()
        if request.is_ajax():
            data = request.body
            data = data.decode('utf-8')
            data = json.loads(data).get('data')
            service = SurveyFormService(data)
            setting_obj = service.create_form()
            return JsonResponse({'setting_obj_id': setting_obj.pk, 'state': True})

        return render(request, 'setting/schoolsettiongs.html', {'school_list': school_list})

    def form_edit(self, request, *args, **kwargs):
        '''
        编辑设置
        :param request:
        :param nid:
        :return:
        '''
        nid = kwargs.get('pk')
        setting_queryset = models.TableSettings.objects.filter(id=nid)
        setting_obj = setting_queryset.first()
        if request.is_ajax():
            try:
                data = request.body
                data = data.decode('utf-8')
                data = json.loads(data).get('data')
                service = SurveyFormService(data)
                service.edit_form(setting_queryset)
                return JsonResponse({'setting_obj_id': setting_obj.pk, 'state': True})
            except Exception as e:
                print(e)
                return JsonResponse({'state': False})
        # 查询出已设置的字段信息
        field_dict = {}
        field_type = ('stu_field_list', 'hel_field_list', 'fam_filed_list', 'par_field_list')
        for i in range(1, 5):
            field_dict[field_type[i - 1]] = models.SettingToField.objects.filter(setting=setting_obj,
                                                                                 fields__field_type=i).values(
                'fields__fieldName', 'fields__pk').order_by('order')
        selected_fields = json.dumps(list(setting_obj.settingtofield_set.values_list('fields__fieldName', )))
        # 填表范围信息
        scope_of_filling = models.ScopeOfFilling.objects.all()
        # 矩阵表信息
        scale_list = setting_obj.scale.all()
        # 单选多选表信息
        choice_tb_list = setting_obj.choice.all()
        tb_info = TableSetting(field_dict, selected_fields, scope_of_filling, setting_obj, scale_list, choice_tb_list)
        return render(request, 'setting/edit_setting.html', {'tb_info': tb_info})

    def preview(self, request):
        '''
        预览页面
        :param request:
        :return:
        '''
        data = json.loads(request.GET.get('data'))
        # stu_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=1)
        # hel_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=2)
        # fam_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=3)
        # par_fields = models.ChoiceField.objects.filter(id__in=data['choiceFieldId'], field_type=4)
        return render(request, 'setting/perview.html', {'data': data})

    def release(self, request, *args, **kwargs):
        '''
        发布页面
        :param request:
        :param nid:
        :return:
        '''
        nid = kwargs.get('pk')
        setting_obj = models.TableSettings.objects.filter(id=nid).first()
        qrfile = os.path.join('/media/school/Qrcode/', setting_obj.Qrcode)
        url = '%s/student/student_info/%s/' % (settings.DOMAIN_NAME, nid)
        return render(request, 'setting/release.html', {'qrfile': qrfile, "url": url})

    list_display = ['title', 'stat_time', 'end_time', 'school_range', 'fill_range', display_count, display_release,
                    display_edit]


class TableSetting(object):
    def __init__(self, field_dic, select_field, scope, setting_obj, scale, choice_tb):
        '''
        将表单设置相关的信息封装进一个类
        :return:
        '''
        self.field_dic = field_dic
        self.select_field = select_field
        self.scope = scope
        self.setting_obj = setting_obj
        self.scale = scale
        self.choice_tb = choice_tb