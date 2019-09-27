from school.models import Grade, SchoolInfo, StuClass
from rest_framework import serializers
from Django_apps.students.models import StudentInfo, FamilyInfo, HomeAddress, StudentToParents, HealthInfo
from school.models import Course
import datetime

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
    family_status = serializers.SerializerMethodField()
    height = serializers.SerializerMethodField()
    date = serializers.SerializerMethodField()

    class Meta:
        model = StudentInfo
        fields = ['id', 'full_name', 'stu_class', 'grade', 'birthday', 'period', "day_age", "family_status", "nation",
                  "height", "date"]

    def get_family_status(self, obj):
        family_obj = FamilyInfo.objects.filter(student=obj).first()
        if family_obj:
            family_status = family_obj.family_status.first()
            return family_status
        else:
            return ''

    def get_height(self, obj):
        health_obj = HealthInfo.objects.filter(student=obj).first()
        if health_obj:
            return health_obj.record.first().height

    def get_date(self, obj):
        tb_obj = obj.for_student.first()
        if tb_obj:
            return datetime.datetime.strftime(tb_obj.date, "%Y-%m-%d")
        return ""


class CourseSerializes(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ["id", "course_des", "abbreviation"]


class StudentHomeSerializes(serializers.ModelSerializer):
    class Meta:
        model = HomeAddress
        fields = ['province', 'city', 'region', 'address']


class StudentParentSerializes(serializers.ModelSerializer):
    relation = serializers.CharField(source="get_relation_display")
    name = serializers.SerializerMethodField()
    occupation = serializers.CharField(source="parents.occupation")
    phone = serializers.CharField(source="parents.telephone")

    class Meta:
        model = StudentToParents
        fields = ['relation', 'name', "occupation", "phone"]

    def get_name(self, obj):
        parent_obj = obj.parents
        if parent_obj:
            return parent_obj.last_name + parent_obj.first_name


class StudentListSerializes(serializers.ModelSerializer):
    stu_class = serializers.CharField(source='stu_class.name')
    grade = serializers.CharField(source='stu_class.grade.get_grade_name_display')

    class Meta:
        model = StudentInfo
        fields = ['id', 'full_name', 'stu_class', 'grade']

