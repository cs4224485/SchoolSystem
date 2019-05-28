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
from APIS.views.surver_forms import SchoolInfoViewSet, GradeAndClassViewSet, PerClassStudentListViewSet

routers = routers.DefaultRouter()
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
    re_path(r"(?P<version>[v1]+)/mental_info/$", AppointmentInfoViewSet.as_view({"get": "list"}), name='mental_info'),
    re_path(r"(?P<version>[v1]+)/per_class_stu/$", GetPerClassStudent.as_view({"get": "list"}), name='per_class_info'),
    re_path(r"(?P<version>[v1]+)/teacher_to_course/$", TeacherToCourseInfoViewSet.as_view()),
    # 过滤学校
    re_path(r"(?P<version>[v1]+)/filter_school/$", FilterSchoolByCity.as_view()),
    # 根据年级过滤班级
    re_path(r"(?P<version>[v1]+)/filter_stu_lass/$", FilterStuClass.as_view()),
    re_path(r"(?P<version>[v1|v2]+)/", include(routers.urls)),
    # 获取学校信息
    re_path(r"(?P<version>[v1|v2]+)/school_info/$", SchoolInfoViewSet.as_view()),
    # 获取班级信息
    re_path(r"(?P<version>[v1|v2]+)/grade_class_info/$", GradeAndClassViewSet.as_view()),
    # 获取每个班级的学生列表
    re_path(r"(?P<version>[v1|v2]+)/per_class_students/$", PerClassStudentListViewSet.as_view()),
]
