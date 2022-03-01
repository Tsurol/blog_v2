import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-s_%!@8ksr+2e^=knvlxf3&^i%&!$(dew01s_9&nzs$lr7$rgln'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'simpleui',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_filters',
    'corsheaders',
    'rest_framework_simplejwt.token_blacklist',
    'mdeditor',
    'authentication',
    'rest_framework',
    'blogsite',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog_v2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

WSGI_APPLICATION = 'blog_v2.wsgi.application'

# Database-mysql
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_v2',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Database-redis

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# 替换系统默认用户模块
AUTH_USER_MODEL = 'authentication.AuthUser'

# 自定义用户认证声明
AUTHENTICATION_BACKENDS = ('authentication.utils.CustomBackend',)

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = '/media/'
# 保存用户上传的文件 目录的绝对文件系统路径
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# drf配置
REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 8,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'code': '2/minute',
        'login': '1/minute',
    }
}

# 授权进行跨站点 HTTP 请求的源列表 todo 部署需重新设置
CORS_ALLOWED_ORIGINS = ['http://localhost:8080', ]

# 短信验证码相关设置
SMS_CONF = {
    # 手机号码正则
    'REGEX_MOBILE': r"^(13[0-9]|14[01456879]|15[0-35-9]|16[2567]|17[0-8]|18[0-9]|19[0-35-9])\d{8}$",
    'host': "106.ihuyi.com",
    'sms_send_uri': "/webservice/sms.php?method=Submit",
    'account': "C76737965",
    'password': 'b66ed19283e7f45c1c81d1a4dbf0bad6'
}

# 邮箱验证码相关配置
EM_CONF = {
    # 邮箱正则
    'REGEX_EMAIL': r"^\w+@[a-zA-Z0-9]+((\.[a-z0-9A-Z]{1,})+)$",
    'sender_email': 'zzlzzl1243@163.com',
    'sender_passwd': 'ITKQBFDPRGLBLSZH',
    'smtp_server': 'smtp.163.com',
    'port': 465,
    'PROJECT_NAME': 'zzl blog'
}

# simple-jwt 配置信息解释
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # 设置token有效时间
    'REFRESH_TOKEN_LIFETIME': timedelta(days=15),  # 刷新token有效时间
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,  # 若为True，刷新后的token将添加到黑名单中
    'UPDATE_LAST_LOGIN': True,  # 设置为True会在用户登录时，更新user表中的last_login字段

    'ALGORITHM': 'HS256',  # 加密算法
    'SIGNING_KEY': SECRET_KEY,  # 签名密钥
    'VERIFYING_KEY': None,  # 验证密钥，用于验证生成令牌的内容
    'AUDIENCE': None,  # 设置为None时，此字段将从token中排除，并且不会进行验证
    'ISSUER': None,  # 设置为None时，此字段将从token中排除，并且不会进行验证
    'JWK_URL': None,  # 设置为None时，此字段将从token中排除，并且在验证期间不使用
    'LEEWAY': 0,  # 用来给到期时间留一些余地
    'AUTH_HEADER_TYPES': ('Bearer',),  # 身份验证的授权标头值value
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',  # 身份验证的授权标头名称key
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',  # 生成token中声明将用于存储用户标识符
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),  # 允许的身份验证令牌类型
    'TOKEN_TYPE_CLAIM': 'token_type',  # 用于存储token类型的声明名称
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',  # 用于存储令牌的唯一标识符的声明名称

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
