from rest_framework.views import APIView, Response
from django.conf import settings
from weixinApp.service.decorator import *
from school import models as scmodels
from weixinApp.serialize.school_info import SchoolInfoSerialize


class WxInit(APIView):
    '''
    获取学校初始化信息
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            school_obj = scmodels.SchoolInfo.objects.filter(id=settings.SCHOOL_ID).first()
            school_date = SchoolInfoSerialize(school_obj)
            if school_date:
                res.code = 200
                res.state = True
                queryset = school_obj.wx_setting.first()
                img_url = {'background': settings.MEDIA_URL + str(queryset.background_img)}
                res.data = {'school_info': school_date.data}
                res.data['school_info'].update(img_url)
                res.msg = '获取成功'
        except Exception as e:
            print(e)
            res.msg = '获取失败'
        return Response(res.get_dict)
