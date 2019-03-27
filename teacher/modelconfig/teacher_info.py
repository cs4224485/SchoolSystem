from stark.service.stark import StarkConfig
from django.shortcuts import HttpResponse, render, redirect
from teacher import models
from teacher.forms.teacher_form import TeacherEditModelForm


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
