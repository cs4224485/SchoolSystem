from rest_framework.views import APIView, Response
from teacher.models import TeacherInfo
from utils.base_response import BaseResponse
from APIS.serialize.PiYue import TeacherInfoSerializers


class TeacherLoginViewSet(APIView):
    '''
    教师批阅系统登陆
    '''

    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        try:
            name = request.data.get('name')
            phone_number = request.data.get('phoneNumber')
            wechat = request.data.get('wechat')
            if not name:
                res.code = 403
                res.msg = '请提供教师姓名'
                return Response(res.get_dict)
            if not phone_number and not wechat:
                res.code = 403
                res.msg = "请提供手机后六位或微信"
                return Response(res.get_dict)
            if len(phone_number) < 6:
                res.code = 402
                res.msg = "手机号码不得小于六位"
                return Response(res.get_dict)

            filter_condition = {'full_name': name}

            if phone_number:
                filter_condition['telephone__endswith'] = phone_number
            if wechat:
                filter_condition['wechat'] = wechat
            teacher_obj = TeacherInfo.objects.filter(**filter_condition).first()
            if not teacher_obj:
                res.code = 404
                res.msg = "该教师不存在请核对信息"
                return Response(res.get_dict)
            res.data = {'teacher_id': teacher_obj.id}
            res.code = 200
        except Exception as e:
            print(e)
            res.code = 500
            res.msg = '获取错误'
        return Response(res.get_dict)


class TeacherInfoViewSet(APIView):
    '''
    教师信息
    '''

    def get(self, request, *args, **kwargs):
        res = BaseResponse()

        teacher_id = request.query_params.get('teacherId')
        if not teacher_id:
            res.code = 403
            res.msg = '请提供教师ID'
            return Response(res.get_dict)
        teacher_obj = TeacherInfo.objects.filter(id=teacher_id).first()
        if not teacher_obj:
            res.code = 404
            res.msg = "未查找到该教师"
            return Response(res.get_dict)
        teacher_se = TeacherInfoSerializers(teacher_obj)
        res.data = {'teacher_info': teacher_se.data}
        res.code = 200
        return Response(res.get_dict)
