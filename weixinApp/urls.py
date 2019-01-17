from django.urls import path, re_path
from weixinApp.views.account import account
from weixinApp.views.schedule import schedule
from weixinApp.views import index

urlpatterns = [
    # 获取openid
    re_path('bind/user$', account.BindUser.as_view()),
    # 根据年级获取班级信息
    re_path('class_info$', account.FilterClass.as_view()),
    # 家长绑定学生
    re_path('bind/children$', account.BindChildren.as_view()),
    # 获取日程表
    re_path('table_time$', schedule.TimeTable.as_view()),
    # 学校初始信息
    re_path('wxinit$', index.WxInit.as_view()),
    # 小程序个人中心
    re_path('personal$', account.PersonCenter.as_view())

]
