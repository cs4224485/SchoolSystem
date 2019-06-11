from school.models import Grade, SchoolInfo, StuClass
from rest_framework import serializers
from teacher.models import TeacherInfo


class SchoolSerializers(serializers.ModelSerializer):
    class Meta:
        model = SchoolInfo
        fields = ['id', 'school_name']


class GradeSerializers(serializers.ModelSerializer):
    grade_name = serializers.CharField(source='get_grade_name_display')

    class Meta:
        model = Grade
        fields = ['id', 'grade_name']


class ClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = StuClass
        fields = ['id', 'name']


