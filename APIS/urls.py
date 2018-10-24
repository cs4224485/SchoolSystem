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

from django.urls import path, re_path, include
from APIS.views.entrance import *
from rest_framework import routers
routers = routers.DefaultRouter()
routers.register(r'student', StudentInfoViewSet)
routers.register(r'health', HealthInfoViewSet)
routers.register(r'allergy', AllergyViewSet)
routers.register(r'Inherited', InheritedDiseaseViewSet)
routers.register(r'country', CountryViewSet)
routers.register(r'test', TestView)
routers.register(r'institutions', GraduateInstitutionsViewSet)
routers.register(r'family', FamilyInfoViewSet,)
routers.register(r'parents', StudentParentsViewSet,)
routers.register(r'stuclass', StuClassViewSet)
urlpatterns = [
   # re_path(r"(?P<version>[v1]+)/student/", StudentInfoViewSet.as_view({"get": "list", "post": "create"}), name='student')
   re_path(r"(?P<version>[v1|v2]+)/", include(routers.urls))
]
