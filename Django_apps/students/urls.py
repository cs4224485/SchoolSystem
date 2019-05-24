from django.urls import re_path
from Django_apps.students.views import student_entrance

urlpatterns = [
   re_path(r"student_info/(\d+)/", student_entrance.StudentInfo.as_view()),
]
