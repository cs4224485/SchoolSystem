from django.urls import path, re_path
from StudentMentalHealth import views

urlpatterns = [
    re_path('login/$', views.LoinView.as_view()),
    re_path('index/$', views.TeacherIndexView.as_view()),
    re_path('student_list/$', views.RecordStudentListView.as_view()),
    re_path('stu_record/(?P<record_id>\d+)/$', views.RecordsOfStudents.as_view()),
    re_path('appointment/$', views.AppointmentTeacher.as_view()),
    re_path('record_list/(?P<student_id>\d+)/$', views.RecordList.as_view()),
    re_path('add_record/(?P<student_id>\d+)/$', views.AddRecord.as_view()),
    re_path('appointment_manage/$', views.AppointmentManage.as_view())
]
