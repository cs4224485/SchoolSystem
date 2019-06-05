"""
用户管理
"""
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse

from Django_apps.rbac.form.user import UserModelForm, UpdateUserModelForm, ResetPasswordUserModelForm
from Django_apps.web.models import UserInfo
from utils.common import gen_md5_password


def user_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    user_queryset = UserInfo.objects.all()

    return render(request, 'rbac/user_list.html', {'users': user_queryset})


def user_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = UserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    post_data = request.POST
    post_data._mutable = True
    post_data['password'] = gen_md5_password(post_data['password'])
    post_data['confirm_password'] = gen_md5_password(post_data['confirm_password'])
    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/change.html', {'form': form})


def user_edit(request, pk):
    """
    编辑用户
    :param request:
    :param pk: 要修改的用户ID
    :return:
    """
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = UpdateUserModelForm(instance=obj)
        return render(request, 'rbac/change.html', {'form': form})

    form = UpdateUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/change.html', {'form': form})


def user_reset_pwd(request, pk):
    """
    重置密码
    :param request:
    :param pk:
    :return:
    """
    obj = UserInfo.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('用户不存在')
    if request.method == 'GET':
        form = ResetPasswordUserModelForm()
        return render(request, 'rbac/change.html', {'form': form})
    post_data = request.POST
    post_data._mutable = True
    post_data['password'] = gen_md5_password(post_data['password'])
    post_data['confirm_password'] = gen_md5_password(post_data['confirm_password'])
    form = ResetPasswordUserModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:user_list'))

    return render(request, 'rbac/change.html', {'form': form})


def user_del(request, pk):
    """
    删除用户
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel_url': origin_url})

    UserInfo.objects.filter(id=pk).delete()
    return redirect(origin_url)
