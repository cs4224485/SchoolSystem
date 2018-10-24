使用stark组件需要完成以下几个步骤

1 拷贝stark app到任何系统
2 在目标project中注册stark app， 如：
    INSTALLED_APPS = [
        ...
        'stark.apps.StarkConfig'
    ]

3 如果想要使用stark组件，则需要在目标app根目录中创建stark.py
4 配置路由信息
    from stark.service.stark import site
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('stark/', stark.site.urls)
    ]

5 在stark.py文件下对表进行注册
    from stark.service.stark import site, StarkConfig, Option
    from .models import *
    site.register(UserInfo, UserInfoConfig)
    site.register(Department)
    site.register(Customer, CustomerInfoConfig)
