from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from Django_apps.web import models
from django.conf import settings
import re


class LoginMiddleware(MiddlewareMixin):
    '''
    访问后台校验用户是否登陆
    '''

    def process_request(self, request):
        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None
        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')
        user_obj = models.UserInfo.objects.filter(id=user_id).first()
        if not user_obj:
            return redirect('/login/')
        return None

