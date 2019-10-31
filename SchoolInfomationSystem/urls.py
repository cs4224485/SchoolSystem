"""SchoolInfomationSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve
from SchoolInfomationSystem import settings
from Django_apps.APIS.views import *
from stark.service.stark import site
from Django_apps.web.views import account
from web.views.PiYue import homework, question_bank

urlpatterns = [
    path('admin/', admin.site.urls),
    # 后台系统登陆
    path('login/', account.login, name='login'),
    # 后台登出
    path('logout/', account.logout, name='logout'),
    re_path(r'^student/', include('Django_apps.students.urls')),
    re_path(r'^school/', include('school.urls')),
    # 学生心理健康相关URL
    re_path(r'^mental/', include('StudentMentalHealth.urls')),
    re_path(r'api/', include('Django_apps.APIS.urls')),
    path('stark/', site.urls),
    re_path(r'^rbac/', include(('rbac.urls', 'rbac'), namespace='rbac'), ),
    re_path(r"media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"homework/$", homework, name='homework'),
    # re_path(r"questions/$", question_bank, name='question'),
    re_path(r"^web/", include("web.urls")),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      path('__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
