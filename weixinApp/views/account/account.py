from rest_framework.views import APIView, Response
from utils.base_response import BaseResponse


class BindUser(APIView):

    def post(self, request, *args, **kwargs):
        res = BaseResponse()
        res.msg = 'ok'
        print(request.data)
        return Response(res.get_dict)