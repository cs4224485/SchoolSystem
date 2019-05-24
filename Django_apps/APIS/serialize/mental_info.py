from Django_apps.students import models as stu_models
from rest_framework import serializers
from teacher import models as tea_models


class StudentListSerialize(serializers.ModelSerializer):
    class Meta:
        model = stu_models.StudentInfo
        fields = ['id', 'full_name']


class PsychologyTeacherSerialize(serializers.ModelSerializer):
    class Meta:
        model = tea_models.TeacherInfo
        fields = ['id', 'first_name', 'last_name']
