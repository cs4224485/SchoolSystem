from rest_framework.views import Response
from rest_framework import viewsets
from django.db import transaction
from django.db.models import Q
from APIS.serialize.student_info import *
from students.models import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from utils.common import *
from utils.checkinfo import *
from school import models as sc_models
import copy


# Create your views here.


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class BaseViewSet(viewsets.ModelViewSet):
    '''
    自定制一个接口基类，可以自定义一些共用方法和功能
    '''

    def dispatch(self, request, *args, **kwargs):

        self.message = {
            'state': False,
            'msg': '',
            'data': []
        }
        response = super(BaseViewSet, self).dispatch(request, *args, **kwargs)
        return response

    def response_error(self, errors):
        '''
        处理错误信息默认只返回第一个字段的错误信息
        :param errors:
        :return:
        '''
        self.message['state'] = False
        for field, error in errors.items():
            self.message['msg'] = error[0]
            break

    def self_list(self, queryset, serializer_class):
        '''
        自定制一个list(相当于GET方法)
        :param queryset: 数据库对象集合
        :param serializer_class: 序列化的类
        :return:
        '''
        if queryset:
            data = serializer_class(queryset, many=True)
            self.message['data'] = data.data
            self.message['state'] = True

        else:
            self.message['msg'] = '获取失败'

        return Response(self.message)


class StudentInfoViewSet(BaseViewSet):
    '''
    添加学生入学调查接口
    '''

    queryset = StudentInfo.objects.all()
    serializer_class = ChineseStudentSerializers
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        # 获取照片
        photo = request.FILES.get('photo')
        if photo:
            request._mutable = True
            del request.data['photo']

        # 基本信息
        # print(request.data)
        request_data = copy.deepcopy(request.data)
        country = request_data.get('country', '1')
        birthday = request_data.get('birthday', '')

        # 隐私信息
        full_name = request_data.get('name')
        id_card = request_data.get('id_card', '')

        # 获取学生对象
        student_id = request_data.get('student_id')
        student_obj = StudentInfo.objects.filter(pk=student_id).first()
        if student_obj:
            birthday = str(student_obj.birthday)

        if id_card:
            is_exist = check_id_exist(id_card)
            if is_exist:
                self.message['msg'] = "信息已存在"
                return Response(self.message)
            # 对身份证进行合法性校验
            check_state, info = check_id_card(id_card)
            if not check_state:
                self.message['msg'] = info['msg']
                return Response(self.message)
            birthday = info['birthday']
            request_data['gender'] = info['gender'][0]
        # 根据生日计算出生肖，年龄，星座，生肖
        if birthday:
            y, m, d = birthday.split('-')
            constellations = get_constellation(int(m), int(d))
            ChineseZodiac = get_ChineseZodiac(int(y))
            age = calculate_age(int(y))
            day_age = calculate_day_age(int(y), int(m), int(d))

            # 将处理完的数据都封装到request_data进行验证
            request_data['birthday'] = birthday
            request_data['constellation'] = constellations[0]
            request_data['age'] = age
            request_data['day_age'] = day_age
            request_data['chinese_zodiac'] = ChineseZodiac[0]

        if photo:
            request_data['photo'] = photo
        request_data['full_name'] = full_name
        # 生成内部编号
        interior_student_id = 'sid:' + str(create_uuid())
        request_data['interior_student_id'] = interior_student_id
        # 获取学校信息
        # school_id = request_data.get('school_id')
        # request_data['school'] = school_id
        # 判断学生的国籍是否为中国
        if str(country) == '1':
            # 判断是否已经存在
            full_name = request_data['last_name'] + request_data['first_name']
            request_data['full_name'] = full_name
            stu_serialize = ChineseStudentSerializers(instance=student_obj, data=request_data, partial=True)
        else:
            stu_serialize = OtherStudentSerializers(instance=student_obj, data=request_data, partial=True)
        if stu_serialize.is_valid():
            # 创建学生对象
            student_obj = stu_serialize.save()
            if student_obj:
                self.message['state'] = True
                self.message['msg'] = '创建成功'
                self.message['data'].append({'student_id': student_obj.pk})
                response = Response(self.message)
            else:
                self.message['msg'] = '创建失败'
                response = Response(self.message)
        else:
            # print(stu_serialize.errors)
            self.response_error(stu_serialize.errors)
            response = Response(self.message)
        return response


class StuClassViewSet(BaseViewSet):
    '''
    获取学校班级接口
    '''

    queryset = StuClass.objects.all()
    serializer_class = StuClassSerializers
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def list(self, request, *args, **kwargs):
        school_id = request.GET.get('school_id')
        self.queryset = StuClass.objects.filter(school=school_id).order_by('name')
        class_dict = {}
        for item in self.queryset:

            if item.grade.pk in class_dict:
                class_dict[item.grade.pk]['children'].append({'value': item.pk, 'text': item.name})
            else:
                class_dict[item.grade.pk] = {
                    'value': item.grade.pk,
                    'text': item.grade.get_grade_name_display(),
                    'children': [{'value': item.pk, 'text': item.name}]
                }
        if class_dict:
            self.message['data'] = class_dict
            self.message['state'] = True

        return Response(self.message)


class CountryViewSet(BaseViewSet):
    '''
    获取国籍信息接口
    '''
    queryset = Country.objects.all()
    serializer_class = CountrySerializers

    def list(self, request, *args, **kwargs):
        return self.self_list(self.queryset, self.serializer_class)


class GraduateInstitutionsViewSet(BaseViewSet):
    '''
    根据输入过滤出毕业学校
    '''
    queryset = SchoolInfo.objects.all().values('school_name')
    serializer_class = SchoolListSerializer

    def list(self, request, *args, **kwargs):
        name_start = request.GET.get('filter', '')
        condition = Q()
        condition.connector = 'or'
        condition.children.append(('school_name__startswith', name_start))
        try:
            self.queryset = sc_models.SchoolInfo.objects.filter(condition).values('id', 'school_name')[0:9]
        except Exception:
            self.queryset = sc_models.SchoolInfo.objects.filter(condition)
        return self.self_list(self.queryset, self.serializer_class)


class AllGraduateInstitutionsViewSet(BaseViewSet):
    queryset = sc_models.SchoolInfo.objects.all()
    serializer_class = SchoolListSerializer

    def list(self, request, *args, **kwargs):
        school_id = request.GET.get('school_id')

        # 当前学校信息
        current_school_info = sc_models.SchoolInfo.objects.filter(id=school_id).values('province', 'city', 'region',
                                                                                       'school_layer').first()
        current_school_info['school_layer'] -= 1
        # 根据当前学校的信息列出所有学校
        self.queryset = self.queryset.filter(**current_school_info)
        return self.self_list(self.queryset, self.serializer_class)


class HealthInfoViewSet(BaseViewSet):
    '''
    添加学生健康信息接口
    '''
    queryset = HealthInfo.objects.all()
    serializer_class = HealthInfoSerializers
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):
        request_data = copy.deepcopy(request.data)
        health_serialize = HealthInfoSerializers(data=request_data)
        student_id = request_data.get('student')
        if health_serialize.is_valid():
            health_serialize.save()
            self.message['state'] = True
            self.message['msg'] = '创建成功'
            self.message['data'].append({'student_id': student_id})
        else:
            self.response_error(health_serialize.errors)
        return Response(self.message)


class AllergyViewSet(BaseViewSet):
    '''
    获取过敏源接口
    '''
    queryset = Allergy.objects.all()
    serializer_class = AllergySerializers

    def list(self, request, *args, **kwargs):
        return self.self_list(self.queryset, self.serializer_class)


class InheritedDiseaseViewSet(BaseViewSet):
    '''
    获取遗传病接口
    '''
    queryset = InheritedDisease.objects.all()
    serializer_class = InheritedDiseaseSerializers

    def list(self, request, *args, **kwargs):
        return self.self_list(self.queryset, self.serializer_class)


class FamilyInfoViewSet(BaseViewSet):
    '''
    添加学生家庭信息接口
    '''
    queryset = FamilyInfo.objects.all()
    serializer_class = FamilyInfoSerializers
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):

        request_data = copy.deepcopy(request.data)
        # print(request_data)
        stu = request_data.get('student')

        family_info_serialize = FamilyInfoSerializers(data=request_data)
        if family_info_serialize.is_valid():
            # 创建家庭信息
            family_obj = family_info_serialize.save()
            request_data['family'] = family_obj.pk
            home_add_serialize = HomeAddressSerializers(data=request_data)
            if home_add_serialize.is_valid():
                # 创建家庭住址
                home_add_serialize.save()
                student_id = request_data.get('student')
                self.message['state'] = True
                self.message['msg'] = '创建成功'
                self.message['data'].append({'student_id': student_id})
            else:
                self.response_error(home_add_serialize.errors)
                return Response(self.message)
        else:
            # print(family_info_serialize.errors)
            self.response_error(family_info_serialize.errors)
            return Response(self.message)

        return Response(self.message)


class StudentParentsViewSet(BaseViewSet):
    '''
    添加学生家长信息接口
    '''
    queryset = StudentParents.objects.all()
    serializer_class = StudentParentsSerializers
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)

    def create(self, request, *args, **kwargs):

        request_data = request.data.get('parents')
        import json
        request_data = json.loads(request_data)
        #print(request_data)
        for key, item in request_data.items():
            parents_serialize = StudentParentsSerializers(data=item)
           # print('key', key)
           # print('item', item)
        for key, item in request_data.items():
            parents_serialize = StudentParentsSerializers(data=item)
            if parents_serialize.is_valid():
                with transaction.atomic():
                    # 创建家长信息
                    parents_obj = parents_serialize.save()
                    item['parents'] = parents_obj.pk
                    stu_to_parents = StudentToParentsSerializers(data=item)
                    if stu_to_parents.is_valid():
                        # 创建家长与学生的对应关系
                        stu_to_parents.save()
                        self.message['state'] = True
                        self.message['msg'] = '创建成功'
                    else:
                       # print('stu_to_parents_error', stu_to_parents.errors)
                        self.response_error(stu_to_parents.errors)
                        return Response(self.message)
            else:
                # print('parents_errors', parents_serialize.errors)
                self.response_error(parents_serialize.errors)
                return Response(self.message)

        return Response(self.message)


class CustomizationQuestionViewSet(BaseViewSet):
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    queryset = ScaleQuestion.objects.all()
    serializer_class = ScaleQuestionSerializers

    def create(self, request, *args, **kwargs):
        request_data = copy.deepcopy(request.data.get('info'))
        import json
        request_data = json.loads(request_data)
        # print(request_data)
        for scale_item in request_data.get('scaleInfo'):
            for scale_pk, des_info in scale_item.items():
                save_data = {'student': request_data.get('studentId'), 'scale': scale_pk}
                scale_serialize = ScaleQuestionSerializers(data=save_data)
                if scale_serialize.is_valid():
                    scale_obj = scale_serialize.save()
                    for item in des_info:
                        for key, value in item.items():
                            ScaleValue.objects.create(title_id=key, value_id=value, scale_stu=scale_obj)

                else:
                    self.response_error(scale_serialize.errors)
                    return Response(self.message)
        else:
            self.message['state'] = True
            self.message['msg'] = '创建成功'
            return Response(self.message)
