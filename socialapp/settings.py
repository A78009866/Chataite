"""
Django settings for socialapp project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-f8_&v%-2b$!%$rz=po!@&5jcy=@)_gzd(wh_jfadn6qyj8q1bp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
# settings.py

STATIC_URL = '/static/'
# settings.py

import os
from pathlib import Path

# Define the base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SQLite Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'socialapp',
    'socialmediaapp',
    'cloudinary_storage', 
    'cloudinary',
]
import cloudinary
import cloudinary.uploader
import cloudinary.api

cloudinary.config( 
  cloud_name = "duixjs8az", 
  api_key = "143978951428697", 
  api_secret = "9dX6eIvntdtGQIU7oXGMSRG9I2o",
  secure = True
)
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'socialapp.urls'

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
# settings.py



WSGI_APPLICATION = 'socialapp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases


# تحليل Internal Database URL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',  # استخدام PostgreSQL
        'NAME': 'railway',  # اسم قاعدة البيانات
        'USER': 'postgres',  # اسم المستخدم
        'PASSWORD': 'VtSielhJRwnjUAXXXJELzrQUFtpbUAKk',  # كلمة المرور
        'HOST': 'postgres.railway.internal',  # Hostname
        'PORT': '5432',  # Port
    }
}
import dj_database_url

DATABASES = {
    'default': dj_database_url.parse('postgresql://postgres:VtSielhJRwnjUAXXXJELzrQUFtpbUAKk@turntable.proxy.rlwy.net:46027/railway')
}

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

# settings.py
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# إعدادات الملفات الثابتة
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # مجلد collectstatic
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'socialmediaapp/static')]  # مجلدات الملفات الثابتة

# إعدادات الملفات الوسائط
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'socialmediaapp.CustomUser'
LOGIN_URL = '/login/'  # تأكد من أن لديك مسار تسجيل الدخول الصحيح هنا

import cloudinary
import cloudinary.uploader
import cloudinary.api

# إعدادات Cloudinary
# Cloudinary settings
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'duixjs8az',          # تأكد من صحتها
    'API_KEY': '143978951428697',       # تأكد من صحتها
    'API_SECRET': '9dX6eIvntdtGQIU7oXGMSRG9I2o',  # تأكد من صحتها
    'SECURE': True
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
ASGI_APPLICATION = 'socialapp.asgi.application'

# إعداد Redis كقناة للاتصال الفوري
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],  # تأكد من تشغيل Redis على هذا المنفذ
        },
    },
}