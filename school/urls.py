from django.urls import path, re_path
from school.views import table_setting

urlpatterns = [
   path(r"settings/", table_setting.school_setting),
   path(r"preview/", table_setting.preview),
   path(r"filter/", table_setting.filterSchool),
   re_path(r"release/(\d+)/", table_setting.release),
   re_path(r"setting_edit/(\d+)/", table_setting.edit_school_setting),
]
