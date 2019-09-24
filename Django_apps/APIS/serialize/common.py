from school.models import Grade, SchoolInfo, StuClass
from rest_framework import serializers
from Django_apps.students.models import StudentInfo
from school.models import Course


class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolInfo
        fields = ['id', 'school_name', "English_name", "logo", "province", "city", "region"]


class GradeSerializers(serializers.ModelSerializer):
    grade_name = serializers.CharField(source='get_grade_name_display')

    class Meta:
        model = Grade
        fields = ['id', 'grade_name']


class ClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = StuClass
        fields = ['id', 'name']


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


class CourseSerializes(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "course_des", "abbreviation"]

class StudentHomeSerializes(serializers.ModelSerializer):
    pass