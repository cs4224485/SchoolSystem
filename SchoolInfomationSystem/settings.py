"""
Django settings for SchoolInfomationSystem project.

Generated by 'django-admin startproject' using Django 2.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z90mwnm$m7@2zbr8*37w7lk0e$7%ka3cdo4_i@j#hs2jo)_su7'
sys.path.insert(0, os.path.join(BASE_DIR, 'Django_apps'))
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'Django_apps.school.apps.SchoolConfig',
    'Django_apps.stark.apps.StarkConfig',
    'Django_apps.teacher.apps.TeacherConfig',
    'Django_apps.StudentMentalHealth.apps.StudentmentalhealthConfig',
    'Django_apps.weixinApp.apps.WeixinappConfig',
    'Django_apps.rbac.apps.RbacConfig',
    'Django_apps.web',
    'Django_apps.students.apps.StudentsConfig',
    'Django_apps.APIS.apps.ApisConfig',
    'debug_toolbar.apps.DebugToolbarConfig',
]

# from corsheaders.middleware import CorsMiddleware

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'web.middleware.login_check.LoginMiddleware',
    'rbac.middleware.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'SchoolInfomationSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'SchoolInfomationSystem.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'zh-cn'

USE_TZ = False

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static")
]

STATIC_ROOT = '/static/'

# RestFramework配置
REST_FRAMEWORK = {
    'DEFAULT_VERSION': 'v1',  # 默认版本
    'ALLOWED_VERSIONS': ['v1', 'v2'],  # 允许的
    'VERSION_PARAM': 'version',  # URL中获取值的key
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )

}

# 跨域添加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = (
#     '*'
# )

CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
    'UPDATE'
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
DOMAIN_NAME = 'http://dc.junji.vip:8081'

# ################## 默认文件上传配置 ########################

# List of upload handler classes to be applied in order.
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Maximum size, in bytes, of a request before it will be streamed to the
# file system instead of into memory.
# 允许内存中上传文件的大小
#   合法：InMemoryUploadedFile对象（写在内存）         -> 上传文件小于等于 FILE_UPLOAD_MAX_MEMORY_SIZE
# 不合法：TemporaryUploadedFile对象（写在临时文件）     -> 上传文件大于    FILE_UPLOAD_MAX_MEMORY_SIZE 且 小于 DATA_UPLOAD_MAX_MEMORY_SIZE
FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440  # i.e. 2.5 MB

# Maximum size in bytes of request data (excluding file uploads) that will be
# read before a SuspiciousOperation (RequestDataTooBig) is raised.
# 允许上传内容的大小（包含文件和其他请求内容）
DATA_UPLOAD_MAX_MEMORY_SIZE = 2621440  # i.e. 2.5 MB

# Maximum number of GET/POST parameters that will be read before a
# SuspiciousOperation (TooManyFieldsSent) is raised.
# 允许的上传文件数
DATA_UPLOAD_MAX_NUMBER_FIELDS = 1000

# The numeric mode to set newly-uploaded files to. The value should be a mode
# you'd pass directly to os.chmod; see https://docs.python.org/3/library/os.html#files-and-directories.
# 文件权限
FILE_UPLOAD_PERMISSIONS = 0o644

# The numeric mode to assign to newly-created directories, when uploading files.
# The value should be a mode as you'd pass to os.chmod;
# see https://docs.python.org/3/library/os.html#files-and-directories.
# 文件夹权限
FILE_UPLOAD_DIRECTORY_PERMISSIONS = None

# 版本号
RELEASE_VERSION = '1.05'

# 学校层级与年级映射
KINDERGARTEN = [13, '小班'], [14, '中班'], [15, '大班']
'''
1 幼儿园: 13小班，14中班，15大班
2 小学:   1 一年级   2 二年级 3 三年级 4 四年级 5 五年级 6 六年级
3 初中：  7 初一 8 初二 9 初三
4 高中：  10 高一   11 高二  12 高三
5 九年一贯制包含小学和初中
6 职高:  包含高一到高三
7 12年一贯制: 包含小学到高中
'''
SCHOOL_GRADE_MAPPING = {
    1: [13, 14, 15],
    2: [1, 2, 3, 4, 5, 6],
    3: [7, 8, 9],
    4: [10, 11, 12],
    5: [1, 2, 3, 4, 5, 6, 7, 8, 9],
    6: [10, 11, 12],
    7: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
}

# 白名单，无需登录就可以访问
VALID_URL_LIST = [
    '/login/',
    '/logout/',
    '/admin/.*',
    '/mental/.*',
    '/media/.*',
    '/api/.*',
    '/student/student_info/(\d+)/',
    '/stark/students/studentinfo/filter_class/',
    '/stark/school/tablesettings/filter/'
]

# 排除自动发现的URL
AUTO_DISCOVER_EXCLUDE = [
    '/admin/.*',
    '/login/',
    '/logout/',
    '/index/',
    '/api/.*',
    '/media/.*'
    '/mental/.*',
    '/__debug__/.*'
]

# 不能进入二级菜单的菜单列表
NOT_IN_SECOND_MENU_LIST = [
    'stark:students_studentinfo_school_list',
]

# 业务中的用户表
RBAC_USER_MODLE_CLASS = "app01.models.UserInfo"
# 权限在Session中存储的key
PERMISSION_SESSION_KEY = "luffy_permission_url_list_key"
# 菜单在Session中存储的key
MENU_SESSION_KEY = "luffy_permission_menu_key"

DATE_FORMAT = 'Y/m/d'
DATETIME_FORMAT = 'Y-m-d H:i:s'

# 年级映射
GRADE_MAP = {'1年级': 1, '2年级': 2, '3年级': 3,
             '4年级': 4, '5年级': 5, '6年级': 6,
             "初一": 7, "初二": 8, "初三": 9,
             "高一": 10, "高二": 11, "高三": 12,
             '小班': 13, '中班': 14}

# CELERY配置
CELERY_BROKER_URL = 'redis://172.16.123.203:6379/'  # Broker配置，使用Redis作为消息中间件
CELERY_RESULT_BACKEND = 'redis://172.16.123.203:6379/'  # BACKEND配置，这里使用redis
CELERY_RESULT_SERIALIZER = 'json'  # 结果序列化方案

CELERY_IMPORTS = (  # 指定导入的任务模块,可以指定多个
    'Django_apps.web.Celery_task.update_grade',
)

CELERY_TIMEZONE = 'Asia/Shanghai'
CELERY_ENABLE_UTC = True
