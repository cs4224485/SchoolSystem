from .settings import *

import six

# Django-debug-tool
DEBUG_TOOLBAR_PATCH_SETTINGS = False
INTERNAL_IPS = '*'

DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',

]

CONFIG_DEFAULTS = {
    # Toolbar options
    'DISABLE_PANELS': {'debug_toolbar.panels.redirects.RedirectsPanel'},
    'INSERT_BEFORE': '</body>',
    'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
    'RENDER_PANELS': None,
    'RESULTS_CACHE_SIZE': 10,
    'ROOT_TAG_EXTRA_ATTRS': '',
    'SHOW_COLLAPSED': False,
    'SHOW_TOOLBAR_CALLBACK': 'debug_toolbar.middleware.show_toolbar',
    # Panel options
    'EXTRA_SIGNALS': [],
    'ENABLE_STACKTRACES': True,
    'HIDE_IN_STACKTRACES': (
        'socketserver' if six.PY3 else 'SocketServer',
        'threading',
        'wsgiref',
        'debug_toolbar',
        'django',
    ),
    'PROFILER_MAX_DEPTH': 10,
    'SHOW_TEMPLATE_CONTEXT': True,
    'SKIP_TEMPLATE_PREFIXES': (
        'django/forms/widgets/',
        'admin/widgets/',
    ),
    'SQL_WARNING_THRESHOLD': 500,  # milliseconds
}

RELEASE_VERSION = '1.21'


# 配置连接MySQL数据库
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'schoolDBdev',  # 要连接的数据库，连接前要创建好
        'USER': 'root',  # 连接数据库的用户名
        'PASSWORD': 'Cs@1993413',  # 连接数据库的密码
        'HOST': "172.16.123.203",  # 连接主机的IP
        'PORT': 3306,  # 数据库端口号
        'OPTIONS': {'init_command': "SET foreign_key_checks = 0;"}
    }
}