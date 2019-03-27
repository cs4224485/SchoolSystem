

from django.urls import path, re_path
from students.views import student_entrance

urlpatterns = [
   re_path(r"student_info/(\d+)/", student_entrance.StudentInfo.as_view()),
]
