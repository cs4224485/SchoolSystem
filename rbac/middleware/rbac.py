# Author: harry.cai
# DATE: 2018/10/9
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse
from django.conf import settings
import re


class RbacMiddleware(MiddlewareMixin):
    '''
    用户权限信息校验
    '''

    def process_request(self, request):
        '''
        当用户请求刚进入时候执行
        :param request:
        :return:
        '''

        '''
        1 获取当前用户请求的URL
        2 获取当前用户在session中保存的权限列表
        3 权限信息匹配
        '''
        current_url = request.path_info

        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                return None

        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            return HttpResponse('未获取到用户权限信息，请登录')

        # url path /首页/客户列表
        url_record = [
            {'title': "首页", 'url': "#"}
        ]

        #  此处代码进行判断是否是无需权限校验但是需要登录的URL: 如 '/login/ /logout/'
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                request.current_permission_pid = 0
                request.breadcrumb = url_record
                return None

        flag = False

        for item in permission_dict.values():
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                flag = True
                request.current_permission_pid = item['pid'] or item['id']
                # 如果有pid需要把父级的路径也加上
                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([{'title': item['p_title'], 'url': item['p_url']}])
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                # 导航条
                request.breadcrumb = url_record
                break

        if not flag:
            return HttpResponse('无权限访问')
