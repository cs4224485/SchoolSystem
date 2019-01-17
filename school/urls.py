from django.urls import path, re_path
from school.views import table_setting

'''
后台管理类视图URL请到对应表的modelConfig目录文件夹下找extra_urls
'''

urlpatterns = [
   path(r"filter/", table_setting.filterSchool),
   # re_path(r"school_info/(?P<school_id>\d+)/$", school_information.ClassManage.as_view()),

]
