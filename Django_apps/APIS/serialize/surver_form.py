from school.models import Grade, SchoolInfo, StuClass
from Django_apps.students.models import StudentInfo
from rest_framework import serializers


class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolInfo
        fields = ['school_name', 'logo', 'address', 'province', 'city', 'region']



class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentInfo
        fields = ['id', 'full_name']


class StudentDetailSerializes(serializers.ModelSerializer):
    stu_class = serializers.CharField(source='stu_class.name')
    grade = serializers.CharField(source='stu_class.grade.get_grade_name_display')

    class Meta:
        model = StudentInfo
        fields = ['id', 'full_name', 'stu_class', 'grade']

