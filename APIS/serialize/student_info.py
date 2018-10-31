from rest_framework import serializers
from students.models import *

student_error = {'last_name': {"error_messages": {"required": "请填写姓"}},
                 'first_name': {"error_messages": {"required": "请填写名"}},
                 'graduate_institutions': {
                 "error_messages": {"required": '请填写毕业院校', "does_not_exist": '学校不存在', "incorrect_type": '学校输入有误'}}}


class ChineseStudentSerializers(serializers.ModelSerializer):
    '''
    序列化中国学生所需填写的数据
    '''

    class Meta:
        model = StudentInfo
        fields = '__all__'

        extra_kwargs = student_error


class OtherStudentSerializers(serializers.ModelSerializer):
    '''
    序列化外国学生所需填写的数据
    '''

    class Meta:
        model = StudentInfo
        exclude = ('first_name', 'last_name', 'nation')
        extra_kwargs = student_error


class HealthInfoSerializers(serializers.ModelSerializer):
    '''
    序列化学生健康信息
    '''

    class Meta:
        model = HealthInfo
        exclude = ('record_date',)
        extra_kwargs = {'height': {"error_messages": {"required": "请输入身高", "max_whole_digits": "身高输入有误"}},
                        'weight': {"error_messages": {"required": "请输入体重", "max_whole_digits": "体重输入有误"}},
                        'vision_left': {"error_messages": {"required": "请输入左眼视力", "max_whole_digits": '视力输入有误'}},
                        'vision_right': {"error_messages": {"required": "请输入右眼视力", "max_whole_digits": '视力输入有误'}},
                        'vision_status': {"error_messages": {"required": "请选择视力状况"}},
                        'blood_type': {"error_messages": {"required": '请选择血型'}}}


class AllergySerializers(serializers.ModelSerializer):
    '''
    过敏源序列化
    '''

    class Meta:
        model = Allergy
        fields = "__all__"


class InheritedDiseaseSerializers(serializers.ModelSerializer):
    class Meta:
        model = InheritedDisease
        fields = "__all__"


class GraduateInstitutionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GraduateInstitutions
        fields = "__all__"


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class FamilyInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model = FamilyInfo
        fields = "__all__"
        extra_kwargs = {
                         'living_condition': {"error_messages": {"required": "请选择居住条件"}},
                         'living_type': {"error_messages": {"required": "请选择居住类型"}},
                         'language': {"error_messages": {"required": "请选择语言"}},
                         'family_status': {"error_messages": {"required": "请选择家庭状况"}},
                        }


class HomeAddressSerializers(serializers.ModelSerializer):
    class Meta:
        model = HomeAddress
        fields = "__all__"
        extra_kwargs = {'address': {"error_messages": {"required": "请输家庭住址"}}}


class StudentParentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentParents
        fields = "__all__"
        extra_kwargs = {
            'first_name': {"error_messages": {"required": "请输入名"}},
            'last_name': {"error_messages": {"required": "请输入姓"}},
            'birthday': {"error_messages": {"required": "请输入生日"}},
            'telephone': {"error_messages": {"required": "请输入联系电话"}},
            'wechat': {"error_messages": {"required": "请输入微信号"}},
        }


class StudentToParentsSerializers(serializers.ModelSerializer):
    class Meta:
        model = StudentToParents
        fields = "__all__"
        extra_kwargs = {
                         'is_main_contact': {"error_messages": {"required": "请选择是否为主要联系人"}},
                        }


class StuClassSerializers(serializers.ModelSerializer):
    class Meta:
        model = StuClass
        fields = "__all__"


class ScaleQuestionSerializers(serializers.ModelSerializer):
    class Meta:
        model = ScaleQuestion
        fields = "__all__"