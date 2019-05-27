from django.shortcuts import render, redirect
from teacher.modelconfig.teacher_info import TeacherInfoConfig
from django.urls import re_path
from stark.service.stark import StarkConfig
from Django_apps.web import TeacherModelForm
from teacher.models import ClassToTeacher


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
            re_path(r'^change/(?P<school_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.change_view), name=self.get_edit_url_name),
            re_path(r'^del/(?P<school_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.delete_view), name=self.get_delete_url_name),
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