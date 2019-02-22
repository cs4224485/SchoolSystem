from django.shortcuts import render, redirect, reverse
from web import models
from utils.common import gen_md5_password


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')
    if not username:
        return render(request, 'login.html', {'none_username': '请输入用户名'})
    if not password:
        return render(request, 'login.html', {'none_password': '请输入密码'})
    md5_password = gen_md5_password(password)
    user_obj = models.UserInfo.objects.filter(name=username, password=md5_password).first()
    if not user_obj:
        return render(request, 'login.html', {'error': '用户名或密码错误'})
    request.session['user_id'] = user_obj.id
    school_list_url = reverse('stark:school_schoolinfo_list')
    return redirect(school_list_url)


def logout(request):
    request.session.delete()
    return redirect(reverse('login'))
