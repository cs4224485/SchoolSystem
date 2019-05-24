import json
import os
from django.shortcuts import render
from stark.service.stark import StarkConfig
from django.urls import re_path
from django.utils.safestring import mark_safe
from school import models
from school.utils.common_utils import *
from django.http import JsonResponse
from Django_apps.web.service.survey_form_service import SurveyFormService
from datetime import datetime


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
            re_path(r'^(?P<pk>\d+)/bind_field$', self.wrapper(self.bind_login_field), name='bind_field'),
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
        url = '/stark/school/tableinfo/%s/list/' % row.pk
        tag = '<a href="%s">%s</a>' % (url, row.table_info.all().count())
        return mark_safe(tag)

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

        return render(request, 'survey_forms/schoolsettiongs.html', {'school_list': school_list})

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
                'fields__fieldName', 'fields__pk', 'is_required').order_by('order')
        selected_fields = json.dumps(list(setting_obj.settingtofield_set.values_list('fields__fieldName')))
        # 填表范围信息
        scope_of_filling = models.ScopeOfFilling.objects.all()
        # 矩阵表信息
        scale_list = setting_obj.scale.all()
        # 单选多选表信息
        choice_tb_list = setting_obj.choice.all()
        tb_info = TableSetting(field_dict, selected_fields, scope_of_filling, setting_obj, scale_list, choice_tb_list)
        return render(request, 'survey_forms/edit_setting.html', {'tb_info': tb_info})

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
        return render(request, 'survey_forms/perview.html', {'data': data})

    def release(self, request, *args, **kwargs):
        '''
        发布页面
        :param request:
        :param nid:
        :return:
        '''
        nid = kwargs.get('pk')
        if request.method == "GET":
            setting_obj = models.TableSettings.objects.filter(id=nid).first()
            qrfile = os.path.join('/media/school/Qrcode/', setting_obj.Qrcode)
            url = '%s/student/student_info/%s/' % (settings.DOMAIN_NAME, nid)
            status = setting_obj.status
            description = setting_obj.description
            title = setting_obj.title
            peroration = setting_obj.peroration
            login_fields = models.FormLoginFields.objects.all()
            selected_fields = [item.id for item in setting_obj.login_fields.all()]
            return render(request, 'survey_forms/release.html',
                          {'qrfile': qrfile, "url": url, 'status': status, 'description': description, 'title': title,
                           'peroration': peroration, 'login_fields': login_fields, 'form_id': setting_obj.pk,
                           'selected_fields': selected_fields})
        title = request.POST.get('title')
        switch = request.POST.get('switch')
        peroration = request.POST.get('peroration')
        description = request.POST.get('description')
        query = models.TableSettings.objects.filter(id=nid)
        state = query.update(title=title, status=switch, description=description, peroration=peroration)
        if state:
            return JsonResponse({'msg': '设置成功', 'code': 200})
        return JsonResponse({'msg': '设置失败', 'code': 500})

    def bind_login_field(self, request, *args, **kwargs):
        '''
        绑定登陆页面的字段
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        nid = kwargs.get('pk')
        if request.method == 'POST':
            action = request.POST.get('action')
            field_id = request.POST.get('id')
            query = models.TableSettings.objects.filter(id=nid).first()
            if action == 'add':
                query.login_fields.add(field_id)
            else:
                query.login_fields.remove(field_id)
            return JsonResponse({'msg': '设置成功', 'code': 200})

    list_display = ['title', 'stat_time', 'end_time', 'school_range', 'fill_range', display_count, display_release,
                    display_edit]


class DetailsOfFilling(StarkConfig):
    '''
    填表详情信息
    '''

    def get_urls(self):
        urlpatterns = [
            re_path(r'^(?P<pk>\d+)/list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
        ]
        urlpatterns.extend(self.extra_urls())

        return urlpatterns

    def display_student(self, row=None, header=False, *args, **kwargs):
        if header:
            return '姓名'
        return row.student.full_name

    def display_date(self, row=None, header=False, *args, **kwargs):
        if header:
            return '填写日期'
        return datetime.strftime(row.date, '%Y-%m-%d')

    def display_preparer(self, row=None, header=False, *args, **kwargs):
        if header:
            return '填表人'
        return row.content_object.parent.first().get_relation_display()

    def get_add_btn(self):
        return None

    def get_list_display(self):
        val = super().get_list_display()
        val.remove(StarkConfig.display_edit)
        val.remove(StarkConfig.display_del)
        return val

    def get_queryset(self, request, *args, **kwargs):
        table_pk = kwargs.get('pk')
        return self.model_class.objects.filter(table=table_pk)

    list_display = [display_student, display_date, display_preparer]


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

