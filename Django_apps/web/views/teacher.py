from django.shortcuts import HttpResponse
from teacher import models
from Django_apps.web.forms.teacher_form import TeacherEditModelForm,TeacherModelForm
from django.shortcuts import render, redirect
from django.urls import re_path
from stark.service.stark import StarkConfig
from teacher.models import ClassToTeacher


class TeacherInfoConfig(StarkConfig):

    def display_name(self, row=None, header=False, *args, **kwargs):
        if header:
            return "姓名"
        return row.full_name

    def display_bind_info(self, row=None, header=False, *args, **kwargs):
        if header:
            return '是否与微信绑定'
        is_bind = row.wx_info.first()
        if is_bind:
            return 'Y'
        return 'N'

    def display_wexin(self, row=None, header=False, *args, **kwargs):
        if header:
            return '微信账号'
        weixin = row.wechat
        if not weixin:
            return '暂无'
        return weixin

    def change_view(self, request, pk, template='stark/change.html', *args, **kwargs):
        '''
        编辑教师
        :param request:
        :param pk:
        :param template:
        :return:
        '''

        obj = self.model_class.objects.filter(pk=pk).first()
        if not obj:
            return HttpResponse('数据不存在')
        class_to_teacher_list = obj.teachers.filter(relate=2)
        form_class = self.get_model_form_class(False, request, pk, *args, **kwargs)
        if request.method == "GET":
            form = form_class(instance=obj)
            return render(request, 'tables/teacher_change.html',
                          {'form': form, 'selected_class': class_to_teacher_list})
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
            form.instance.full_name = request.POST.get('last_name') + request.POST.get('first_name')
            teacher_obj = form.save()
            class_ids = request.POST.getlist('choice_class')
            query = models.ClassToTeacher.objects
            exist_ids = query.filter(relate=2, teacher=teacher_obj).values_list('stu_class_id')
            exist_ids = [str(i[0]) for i in exist_ids]
            delete_ids = list(set(exist_ids).difference(class_ids))
            # 需要删除的关联班级
            if delete_ids:
                query.filter(relate=2, teacher=teacher_obj, stu_class__in=delete_ids).delete()
            # 需要创建的关联班级
            create_ids = list(set(class_ids).difference(exist_ids))
            create_list = []
            for item_id in create_ids:
                obj = models.ClassToTeacher(teacher=teacher_obj, stu_class_id=item_id, relate=2)
                create_list.append(obj)
            query.bulk_create(create_list)
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, 'tables/teacher_change.html', {'form': form, 'selected_class': class_to_teacher_list})

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        return TeacherEditModelForm

    def get_add_btn(self):
        return None

    list_display = ['full_name', 'school', display_bind_info, display_wexin]
    search_list = ['first_name', 'last_name', 'full_name']


class SchoolTeacherConfig(TeacherInfoConfig):
    '''
    每个学校的老师管理
    '''
    change_list_template = 'teacher_list.html'
    search_list = ['full_name']

    def get_urls(self):
        urlpatterns = [
            re_path(r'^list/(?P<school_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add_teacher/(?P<school_id>\d+)/$', self.wrapper(self.add_teacher), name='add_teacher'),
            re_path(r'^change/(?P<school_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view),
                    name=self.get_edit_url_name),
            re_path(r'^del/(?P<school_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view),
                    name=self.get_delete_url_name),
        ]
        urlpatterns.extend(self.extra_urls())

        return urlpatterns

    def get_queryset(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        return self.model_class.objects.filter(school_id=school_id)

    def get_extra_content(self, *args, **kwargs):
        add_teacher_url = self.reverse_commons_url('add_teacher', *args, **kwargs)
        return {'add': add_teacher_url}

    def get_list_display(self):
        display_list = []
        display_list.extend(self.list_display)
        display_list.append(StarkConfig.display_edit_del)
        return display_list

    def add_teacher(self, request, *args, **kwargs):
        school_id = kwargs.get('school_id')
        if request.method == 'GET':
            form = TeacherModelForm(school_id=school_id)
            return render(request, 'tables/teacher_change.html', {'form': form, 'school_id': school_id})
        form = TeacherModelForm(request.POST, school_id=school_id)
        if form.is_valid():
            form.instance.school_id = school_id
            form.instance.full_name = request.POST.get('last_name') + request.POST.get('first_name')
            teacher_obj = form.save()
            class_ids = request.POST.getlist('choice_class')
            create_list = []
            for item_id in class_ids:
                obj = ClassToTeacher(teacher=teacher_obj, stu_class_id=item_id, relate=2)
                create_list.append(obj)
            ClassToTeacher.objects.bulk_create(create_list)
            return redirect(self.reverse_list_url(*args, **kwargs))
        return render(request, 'tables/teacher_change.html', {'form': form, 'school_id': school_id})
