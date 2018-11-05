from django.urls import path, re_path
from StudentMentalHealth import views

urlpatterns = [
    re_path('login/$', views.LoinView.as_view()),
    re_path('index/$', views.TeacherIndexView.as_view()),
    re_path('record_list/$', views.RecordStudentListView.as_view()),
    re_path('stu_record/(?P<student_id>\d+)/$', views.RecordsOfStudents.as_view()),
]
