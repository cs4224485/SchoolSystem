# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }
# 配置连接MySQL数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schooladmin',  # 要连接的数据库，连接前要创建好
        'USER': 'root',  # 连接数据库的用户名
        'PASSWORD': 'Cs@1993413',  # 连接数据库的密码
        'HOST': "172.16.123.203",  # 连接主机的IP
        'PORT': 3306,  # 数据库端口号
        'OPTIONS': {'init_command': "SET foreign_key_checks = 0;"}
    }
}

DEBUG = False
