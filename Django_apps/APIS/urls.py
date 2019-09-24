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
    2. Add a URL t.o urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import re_path, include
from rest_framework import routers
from Django_apps.APIS.views.school_info.timetable_api import *
from Django_apps.APIS.views.filters import FilterSchoolByCity, FilterStuClass
from Django_apps.APIS.views.entrance import *
from Django_apps.APIS.views.mental import AppointmentInfoViewSet, GetPerClassStudent
from APIS.views.surver_forms import SchoolScaleAvgViewSet, StudentScaleAvgViewSet, TableInfoViewSet
from APIS.views.common import GetAllSchoolViewSet, FilterGradeAndClassViewSet, SchoolInfoViewSet, \
    PerClassStudentListViewSet, StudentDetailInfo, CourseViewSet, StudentHomeAddressViewSet
from APIS.views.PiYue import TeacherLoginViewSet, TeacherInfoViewSet
from APIS.views.assessment import BaseInfoViewSet, HealthViewSet, LanguageViewSet, ScienceViewSet, SocietyViewSet, \
    InterestViewSet, ArtViewSet

routers = routers.DefaultRouter()
# 入学填报相关url
routers.register(r'student', StudentInfoViewSet)
routers.register(r'health', HealthInfoViewSet)
routers.register(r'allergy', AllergyViewSet)
routers.register(r'Inherited', InheritedDiseaseViewSet)
routers.register(r'country', CountryViewSet)
routers.register(r'institutions', GraduateInstitutionsViewSet)
routers.register(r'all_institutions', AllGraduateInstitutionsViewSet)
routers.register(r'family', FamilyInfoViewSet, )
routers.register(r'parents', StudentParentsViewSet, )
routers.register(r'stuclass', StuClassViewSet)
routers.register(r'customization', CustomizationQuestionViewSet)

urlpatterns = [
    re_path(r"(?P<version>[v1|v2]+)/", include(routers.urls)),
    re_path(r"(?P<version>[v1]+)/mental_info/$", AppointmentInfoViewSet.as_view({"get": "list"}), name='mental_info'),
    re_path(r"(?P<version>[v1]+)/per_class_stu/$", GetPerClassStudent.as_view({"get": "list"}), name='per_class_info'),
    re_path(r"(?P<version>[v1]+)/teacher_to_course/$", TeacherToCourseInfoViewSet.as_view()),
    # 过滤学校
    re_path(r"(?P<version>[v1]+)/filter_school/$", FilterSchoolByCity.as_view()),
    # 根据年级过滤班级
    re_path(r"(?P<version>[v1]+)/filter_stu_lass/$", FilterStuClass.as_view()),

    # -----common通用接口----------------
    # 获取班级或年级信息
    re_path(r"(?P<version>[v1|v2]+)/grade_class_info/$", FilterGradeAndClassViewSet.as_view()),
    # 获取所有的学校
    re_path(r"(?P<version>[v1|v2]+)/all_school/$", GetAllSchoolViewSet.as_view()),
    # 获取每个班级的学生列表
    re_path(r"(?P<version>[v1|v2]+)/per_class_students/$", PerClassStudentListViewSet.as_view()),
    # 获取学校信息
    re_path(r"(?P<version>[v1|v2]+)/school_info/$", SchoolInfoViewSet.as_view()),
    # 学生详细信息
    re_path(r"(?P<version>[v1|v2]+)/student_detail/$", StudentDetailInfo.as_view()),
    # 获取课程信息
    re_path(r"(?P<version>[v1|v2]+)/course/$", CourseViewSet.as_view()),
    # 获取学生家庭信息
    re_path(r"(?P<version>[v1|v2]+)/home/$", StudentHomeAddressViewSet.as_view()),

    # -----form表单接口------------------
    # 全校量表平均值数据
    re_path(r"(?P<version>[v1|v2]+)/school_scale_avg/$", SchoolScaleAvgViewSet.as_view()),
    # 学生量表平均值数据
    re_path(r"(?P<version>[v1|v2]+)/student_scale_avg/$", StudentScaleAvgViewSet.as_view()),

    # 表单信息
    re_path(r"(?P<version>[v1|v2]+)/table_info/$", TableInfoViewSet.as_view()),

    # 批阅系统教师登陆
    re_path(r"(?P<version>[v1|v2]+)/piyue/login$", TeacherLoginViewSet.as_view()),
    # 批阅系统教师信息
    re_path(r"(?P<version>[v1|v2]+)/teacher_info$", TeacherInfoViewSet.as_view()),

    # -------- 综合素质评估接口
    re_path(r"(?P<version>[v1|v2]+)/assessment/(?P<pk>\d+)$", BaseInfoViewSet.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/health/(?P<pk>\d+)$", HealthViewSet.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/language/(?P<pk>\d+)$", LanguageViewSet.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/science/(?P<pk>\d+)$", ScienceViewSet.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/society/(?P<pk>\d+)$", SocietyViewSet.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/art/(?P<pk>\d+)$", ArtViewSet.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/interest/(?P<pk>\d+)$", InterestViewSet.as_view()),
]
