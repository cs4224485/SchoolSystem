# Author: harry.cai
# DATE: 2018/10/9
from django.conf import settings


def init_permission(current_user, request):
    """
    用户权限的初始化
    :param current_user: 当前用户对象
    :param request: 请求相关所有数据
    :return:
    """
    # 根据当前用户信息获取此用户拥有的所有权限，并放入session
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__url",
                                                                                      "permissions__name",
                                                                                      "permissions__pid",
                                                                                      "permissions__pid__title",
                                                                                      "permissions__pid__url",
                                                                                      "permissions__title",
                                                                                      "permissions__icon",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon").distinct()

    # 获取权限和菜单信息
    permission_dict = {}
    menu_dict = {}
    '''
    构建二级菜单的格式
    {'1': 
        {'tittle': '信息管理', 
        'icon': None, 
        'class':''
        'children': [
            {
            'id':1
            'title': '客户列表', 
            'url': '/customer/list/'  可以做菜单的权限信息
            }
        ]
    },
     '2': 
        {'tittle': '用户管理', 
        'icon': None, 
        'class':'hide'
        'children': [
            {
            'id':7
            'title': '账单列表', 
            'url': '/payment/list/'
            }
        ]
     }
    }
    
     - 获取权限信息（根据PID可以体现父级菜单）
     [
        {'id':1, 'url':/customer/list', pid:nul}    # 客户列表 可以做菜单的权限
        {'id':2, 'url':/customer/add', pid:1}       # 添加客户 不可做菜单
        {'id':3, 'ur;'/customer/del', pid:1}        # 删除客户 可以做菜单的权限
     ]
    '''
    for item in permission_queryset:
        permission_dict[item['permissions__name']] = {'id': item['permissions__id'],
                                                      'title': item['permissions__title'],
                                                      'url': item['permissions__url'],
                                                      'pid': item['permissions__pid'],
                                                      'p_url': item['permissions__pid__url'],
                                                      'p_title': item['permissions__pid__title']
                                                      }
        menu_id = item['permissions__menu_id']
        if not menu_id:
            continue
        node = {'title': item['permissions__title'], 'id': item['permissions__id'], 'url': item['permissions__url']}
        if menu_id in menu_dict:
            menu_dict[menu_id]['children'].append(node)
        else:
            menu_dict[menu_id] = {
                'title': item['permissions__menu__title'],
                'icon': item['permissions__menu__icon'],
                'children': [node, ]
            }

    # 将URL放入session中
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
    print(menu_dict)
