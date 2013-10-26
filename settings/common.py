# List of callables that know how to import templates from various sources.
import os
ADMINS = ()

DATABASES = {'default': {'ENGINE': 'django.db.backends.mysql', 'NAME': 'my_db', 'HOST': '', 'USER': 'root', 'PASSWORD': '', 'PORT': ''}}

DEBUG = True

EMAIL_HOST = 'smtp.sendgrid.net'

EMAIL_HOST_PASSWORD = os.environ.get('SENDGRID_PASSWORD')

EMAIL_HOST_USER = os.environ.get('SENDGRID_USERNAME')

EMAIL_PORT = 587

EMAIL_USE_TLS = True

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes'
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'gunicorn',
    'south',
    'django_extensions',
    'kareflow',
    'emailer',
    'provider',
    'account',
    'task',
    'patient',
    'discharge')

LANGUAGE_CODE = 'en-us'

LOGGING = {'loggers': {'django.request': {'level': 'ERROR', 'propagate': True, 'handlers': ['mail_admins']}}, 'version': 1, 'filters': {'require_debug_false': {'()': 'django.utils.log.RequireDebugFalse'}}, 'disable_existing_loggers': False, 'handlers': {'mail_admins': {'class': 'django.utils.log.AdminEmailHandler', 'filters': ['require_debug_false'], 'level': 'ERROR'}}}

MANAGERS = ()

MEDIA_ROOT = 'media'

MEDIA_URL = '/media/'

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware', 'django.contrib.sessions.middleware.SessionMiddleware', 'django.middleware.csrf.CsrfViewMiddleware', 'django.contrib.auth.middleware.AuthenticationMiddleware', 'django.contrib.messages.middleware.MessageMiddleware')

ROOT_URLCONF = 'urls'

SECRET_KEY = '24^+j9002sz=^%$%3l#u3-@&amp;u+1xg2zh5_()x^(h7-@2tdp%cb'

SITE_ID = 1

STATICFILES_DIRS = ()

STATICFILES_FINDERS = ('django.contrib.staticfiles.finders.FileSystemFinder', 'django.contrib.staticfiles.finders.AppDirectoriesFinder')

STATIC_ROOT = ''

STATIC_URL = '/static/'

TEMPLATE_DEBUG = True

TEMPLATE_DIRS = ('templates',)

TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader', 'django.template.loaders.app_directories.Loader')

TIME_ZONE = 'America/Chicago'

USE_I18N = True

USE_L10N = True

USE_TZ = True
