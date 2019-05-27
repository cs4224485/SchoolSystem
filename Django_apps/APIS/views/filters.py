from rest_framework.views import APIView
from school.models import SchoolInfo, StuClass, Grade
from utils.common import order_by_class
from django.http.response import JsonResponse
from django.core import serializers


class FilterSchoolByCity(APIView):
    '''
    根据学校位置过滤学校
    '''

    def get(self, request, *args, **kwargs):
        data = request.GET
        layer = data.get('layer')
        extra = {}
        if layer:
            extra['school_layer'] = layer

        school_list = list(SchoolInfo.objects.filter(province=data.get('province'),
                                                     city=data.get('city'), region=data.get('region'),
                                                     **extra).values('school_name', 'pk', 'campus_district'))
        return JsonResponse({'school_list': school_list}, json_dumps_params={"ensure_ascii": False})


class FilterStuClass(APIView):

    def get(self, request, *args, **kwargs):
        '''
        根据年级过滤出学校的班级
        :param request:
        :return:
        '''

        school_id = request.GET.get('school_id')
        grade = request.GET.get('grade', 7)
        # 筛选出符合父级要求的所有子级，因为输出的是一个集合，需要将数据序列化 serializers.serialize（）
        class_queryset = order_by_class(
            list(StuClass.objects.filter(school=school_id, grade=grade).order_by('name')))
        grade_queryset = Grade.objects.filter(stuclass__school_id=school_id).distinct()
        grade_list = []
        for item in grade_queryset:
            grade_list.append({'id': item.id, 'grade': item.get_grade_name_display()})
        stu_class = serializers.serialize("json", class_queryset)
        # 判断是否存在，输出
        if stu_class:
            return JsonResponse({'stu_class': stu_class, 'grade_list': grade_list, 'code': 200},
                                json_dumps_params={"ensure_ascii": False})
        else:
            return JsonResponse({'stu_class': []})
