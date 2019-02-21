from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from weixinApp import models
from weixinApp.service.user_service import UserService


class WeiXinAuth(BaseAuthentication):
    '''
    微信认证方法
    '''

    def authenticate(self, request):
        token = request.META.get('HTTP_AUTHORIZATION')
        if not token:
            raise AuthenticationFailed({'code': -1, 'error': '认证失败'}, )
        bind_info = check_login(token)
        if not bind_info:
            raise AuthenticationFailed({'code': -1, 'error': '认证失败'}, )
        return bind_info.open_id, bind_info


def check_login(auth_token):
    '''
    判断是否已经授权
    :param auth_token:
    :return:
    '''

    auth_info = auth_token.split("#")
    if len(auth_info) != 2:
        return False
    try:
        bind_info = models.WechatBindInfo.objects.filter(id=auth_info[1]).first()
    except Exception as e:
        return False

    if bind_info is None:
        return False

    if auth_info[0] != UserService.geneAuthCode(bind_info):
        return False

    if bind_info.status != 1:
        return False
    return bind_info
