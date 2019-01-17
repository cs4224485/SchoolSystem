from rest_framework import serializers
from students import models as scmodels


class StudentSerialize(serializers.ModelSerializer):
    gender = serializers.CharField(source='get_gender_display')
    stu_class = serializers.CharField(source='stu_class.name')
    grade = serializers.CharField(source='stu_class.grade.get_grade_name_display')

    class Meta:
        model = scmodels.StudentInfo
        fields = ['id', 'full_name', 'gender', 'photo', 'stu_class', 'grade']
