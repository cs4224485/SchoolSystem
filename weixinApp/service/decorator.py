from students import models as stumodels
from utils.base_response import BaseResponse
from rest_framework.views import Response

'''
小程序需要的装饰器
'''


def get_user_obj(func):
    '''
    小程序登陆后获取绑定的身份对象
    :return:
    '''

    def inner(request, *args, **kwargs):
        res = BaseResponse()
        if not request.auth.wx_user:
            res.code = -1
            res.msg = '未能获取到身份信息，请先设置身份信息'
            return Response(res.get_dict)
        user_info = request.auth.wx_user
        if user_info.user_type == 1:
            student_parent_obj = stumodels.StudentToParents.objects.filter(parents_wxinfo=user_info).first()
            return func(request, obj=student_parent_obj, *args, **kwargs)
        elif user_info.user_type == 2:
            teacher_obj = user_info.content_object.first()
            return func(request, obj=teacher_obj, *args, **kwargs)
        else:
            return func(request, *args, **kwargs)

    return inner
