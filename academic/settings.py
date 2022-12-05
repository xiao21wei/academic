"""
Django settings for academic project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
import yaml
import platform
import redis

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# 从secrets.yaml文件中读取配置
with open(BASE_DIR / 'secrets.yaml', 'r') as f:
    secrets = yaml.load(f, Loader=yaml.FullLoader)
    databases_name = secrets['DATABASE']['name']
    databases_user = secrets['DATABASE']['user']
    databases_password = secrets['DATABASE']['password']
    databases_host = secrets['DATABASE']['host']
    databases_port = secrets['DATABASE']['port']
    mail_host = secrets['MAIL']['host']
    mail_port = secrets['MAIL']['port']
    mail_user = secrets['MAIL']['user']
    mail_password = secrets['MAIL']['password']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-_1#)1rvok_2je@2zm8#%np+erylj8=exf(38wm(k+5i27$ce--'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'my_app.apps.MyAppConfig',
]

MIDDLEWARE = [
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'django.middleware.cache.FetchFromCacheMiddleware',
]

LOCAL = False
if platform.system() == 'Windows':
    LOCAL = True

if not LOCAL:
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
CORS_ALLOW_ALL_ORIGINS = True
CORS_ORIGIN_ALLOW_ALL = False  # 允许所有源访问
CORS_ORIGIN_WHITELIST = (
    'http://127.0.0.1:8000',  # 设置白名单
    'http://localhost:8000',
)

CORS_ALLOW_METHODS = (
    'DELETE',  # 允许的方法
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
    'VIEW',
)

CORS_ALLOW_HEADERS = (
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',  # 允许的请求头
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

ROOT_URLCONF = 'academic.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'academic.wsgi.application'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# Redis settings
REDIS_TIMEOUT=7*24*60*60
CUBES_REDIS_TIMEOUT=60*60
NEVER_REDIS_TIMEOUT=365*24*60*60

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': databases_name,
        'USER': databases_user,
        'PASSWORD': databases_password,
        'HOST': databases_host,
        'PORT': databases_port,
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_TZ = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'img').replace('\\', '/')

if platform.system() == "Windows":
    IMG_URL = "127.0.0.1:8000/"
else:
    IMG_URL = "123.57.194.168:8000/"

Redis = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings
EMAIL_HOST = mail_host						# 服务器
EMAIL_USE_SSL = True							# 服务器端设置
EMAIL_PORT = mail_port								# 本地为25,服务器为465
EMAIL_HOST_USER = mail_user			# 账号
EMAIL_HOST_PASSWORD = mail_password 	# 密码 (注意：这里的密码指的是授权码)
EMAIL_USE_TLS = False							# 一般都为False
EMAIL_FROM = 'academic <{}>'.format(mail_user)				# 邮箱来自

CAPTCHA_IMAGE_SIZE = (178, 56)

CAPTCHA_NOISE_FUNCTIONS = (
    'captcha.helpers.noise_null',
    'captcha.helpers.noise_dots',
)

SILENCED_SYSTEM_CHECKS = ['captcha.recaptcha_test_key_error']

SWAGGER_SETTINGS = {
    # 基础样式
    'SECURITY_DEFINITIONS': {
        "basic": {
            'type': 'basic'
        }
    },
    # 如果需要登录才能够查看接口文档, 登录的链接使用restframework自带的.
    # 'LOGIN_URL': 'rest_framework:login',
    # 'LOGOUT_URL': 'rest_framework:logout',
    # 'DOC_EXPANSION': None,
    # 'SHOW_REQUEST_HEADERS':True,
    # 'USE_SESSION_AUTH': True,
    # 'DOC_EXPANSION': 'list',
    # 接口文档中方法列表以首字母升序排列
    'APIS_SORTER': 'alpha',
    # 如果支持json提交, 则接口文档中包含json输入框
    'JSON_EDITOR': True,
    # 方法列表字母排序
    'OPERATIONS_SORTER': 'alpha',
    'VALIDATOR_URL': None,
}
