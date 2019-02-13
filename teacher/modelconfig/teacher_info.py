from stark.service.stark import StarkConfig, ChangeList
from django.urls import reverse, re_path
from django.shortcuts import HttpResponse, render, redirect
from django.conf import settings
from utils.common import *
from django.utils.safestring import mark_safe
from teacher import models
from teacher.forms.teacher_form import TeacherEditModelForm


class TeacherInfoConfig(StarkConfig):

    def display_name(self, row=None, header=False):
        if header:
            return "姓名"
        first_name, last_name, mark = shadow_name(row.first_name, row.last_name)
        html = '{0}<span style="font-size:21px; color:black; position: relative; top: 5px;">{1}</span>{2}'
        if mark:
            return mark_safe(html.format(last_name, mark, first_name))
        else:
            return mark_safe(html.format(last_name, '*', first_name))

    def change_view(self, request, pk, template='stark/change.html'):
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
        form_class = self.get_edit_model_form_class()
        if request.method == "GET":
            form = form_class(instance=obj)
            return render(request, 'tables/teacher_change.html',
                          {'form': form, 'selected_class': class_to_teacher_list})
        form = form_class(request.POST, instance=obj)
        if form.is_valid():
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
            return redirect(self.reverse_list_url())
        return render(request, 'tables/teacher_change.html', {'form': form, 'selected_class': class_to_teacher_list})

    def get_edit_model_form_class(self):
        return TeacherEditModelForm

    def get_add_btn(self):
        return None

    list_display = [display_name, 'school']
    search_list = ['full_name']
