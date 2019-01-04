"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 2.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os
import socket

# para obtener datos del servidor
HOSTNAME = socket.gethostname()
DJANGO_IP = socket.gethostbyname(HOSTNAME)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'h$i(((hm+m2l592$mh=#8%lk8ov14@_tyu5*2jy0+bb4s+y1!d'

# SECURITY WARNING: don't run with debug turned on in production!

# A.V en Produccion se debe quitar esto y dejar en False
# por ahora si esta con la IP del coordinador queda en False
if DJANGO_IP == '10.0.20.146':
    X_DEBUG = False
else:
    X_DEBUG = True

# A.V Forzar el debug en caso que sea necesario para probar
# DEBUG = False
DEBUG = X_DEBUG

ALLOWED_HOSTS = ['*', ]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'appcore',
    'ckeditor'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'appcore.middleware_custom_405.ExceptionMiddleware405',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'config.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'AKzioDB',
        'USER': 'AKZIO_REP',
        'PASSWORD': 'cUy53r5R',
        'HOST': '192.168.101.155',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
    'prime_v10': {
        'ENGINE': 'sql_server.pyodbc',
        'NAME': 'PRIME_V10',
        'USER': 'AKZIO_REP',
        'PASSWORD': 'cUy53r5R',
        'HOST': '192.168.101.155',
        'PORT': '1433',
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    },
}

# CKEDITOR
CKEDITOR_CONFIGS = {
    'default': {
        'allowedContent': True,
        'toolbar': [
            ['Format', 'Bold', 'Italic', 'Underline', 'Strike', 'SpellChecker'],
            ['NumberedList', 'BulletedList', 'Indent', 'Outdent', 'JustifyLeft', 'JustifyCenter',
             'JustifyRight', 'JustifyBlock'],
            ['Image', 'Table', 'Link', 'Unlink', 'Anchor', 'SectionLink', 'Subscript', 'Superscript'],
            ['Undo', 'Redo'], ['Source'],
            ['Maximize']
        ],
    },
}

# set this to False if you want to turn off pyodbc's connection pooling
DATABASE_CONNECTION_POOLING = False

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

FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'es_CL'
TIME_ZONE = 'America/Santiago'
USE_I18N = True
USE_L10N = False
USE_TZ = False
DATETIME_FORMAT = 'd-m-Y'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

# AUTH_USER
AUTH_USER_MODEL = 'appcore.User'

# EMAIL

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
MAILER_EMAIL_BACKEND = EMAIL_BACKEND
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'evaluacion360@akzio.cl'
EMAIL_HOST_PASSWORD = '__$$Akzio2018'
EMAIL_PORT = 465
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# LOCALE
LOCALE_PATHS = (
    os.path.join(os.path.dirname(__file__), 'locale'),
)

# MEDIDAS TOP
MEDIDAS_TOP_PATH = '/MEDIDAS_TOP/'

# SOCKET CHANNEL
MEDIDAS_TOP_PATH = '/SOCKET/'
