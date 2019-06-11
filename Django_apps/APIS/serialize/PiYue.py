from rest_framework import serializers
from teacher.models import TeacherInfo


class TeacherInfoSerializers(serializers.ModelSerializer):
    # 班主任负责的班级
    handle_class = serializers.SerializerMethodField()
    # 所带课程和班级
    course_class = serializers.SerializerMethodField()
    identity = serializers.SerializerMethodField()

    class Meta:
        model = TeacherInfo
        fields = ['id', 'full_name', 'identity', 'handle_class', 'course_class']

    def get_handle_class(self, obj):
        class_teacher = obj.teachers.filter(relate=1).first()
        if class_teacher:
            grade = class_teacher.stu_class.grade.get_grade_name_display()
            class_name = class_teacher.stu_class.name
            return grade + class_name
        return None

    def get_course_class(self, obj):
        course = obj.course.all().first()
        class_teacher = obj.teachers.filter(relate=2).first()
        if not course:
            return None

        if not class_teacher:
            return None
        grade = class_teacher.stu_class.grade.get_grade_name_display()
        return {'course': course.course_des, "grade": grade}

    def get_identity(self, obj):
        if obj.identity:
            return obj.identity.title
        return None