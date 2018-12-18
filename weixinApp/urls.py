from django.urls import path, re_path, include
from weixinApp.views.account import account

urlpatterns = [
    re_path('bind/user', account.BindUser.as_view())
]
