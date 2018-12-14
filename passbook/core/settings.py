"""
Django settings for passbook project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import importlib
import os

from django.contrib import messages

from passbook import __version__
from passbook.lib.config import CONFIG

VERSION = __version__

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STATIC_ROOT = BASE_DIR + '/static'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = CONFIG.get('secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
INTERNAL_IPS = ['127.0.0.1']
ALLOWED_HOSTS = []

LOGIN_URL = 'passbook_core:auth-login'
# CSRF_FAILURE_VIEW = 'passbook.core.views.errors.CSRFErrorView.as_view'

# Custom user model
AUTH_USER_MODEL = 'passbook_core.User'

CSRF_COOKIE_NAME = 'passbook_csrf'
SESSION_COOKIE_NAME = 'passbook_session'
LANGUAGE_COOKIE_NAME = 'passbook_language'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'passbook.oauth_client.backends.AuthorizedServiceBackend'
]
AUTHENTICATION_FACTORS = [
    'passbook.core.auth.backend_factor.AuthenticationBackendFactor',
    'passbook.core.auth.dummy.DummyFactor',
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'reversion',
    'rest_framework',
    'passbook.core',
    'passbook.admin',
    'passbook.api',
    'passbook.audit',
    'passbook.lib',
    'passbook.ldap',
    'passbook.oauth_client',
    'passbook.oauth_provider',
    'passbook.saml_idp',
    'passbook.tfa',
]

# Message Tag fix for bootstrap CSS Classes
MESSAGE_TAGS = {
    messages.DEBUG: 'primary',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'passbook.core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'passbook.core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Celery settings
# Add a 10 minute timeout to all Celery tasks.
CELERY_TASK_SOFT_TIME_LIMIT = 600
CELERY_TIMEZONE = TIME_ZONE
CELERY_BEAT_SCHEDULE = {}
CELERY_CREATE_MISSING_QUEUES = True
CELERY_TASK_DEFAULT_QUEUE = 'passbook'
CELERY_BROKER_URL = 'redis://%s' % CONFIG.get('redis')
CELERY_RESULT_BACKEND = 'redis://%s' % CONFIG.get('redis')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

LOG_HANDLERS = ['console', 'syslog', 'file', 'sentry']

with CONFIG.cd('log'):
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': True,
        'formatters': {
            'verbose': {
                'format': ('%(asctime)s %(levelname)-8s %(name)-55s '
                           '%(funcName)-20s %(message)s'),
            },
            'color': {
                '()': 'colorlog.ColoredFormatter',
                'format': ('%(log_color)s%(asctime)s %(levelname)-8s %(name)-55s '
                           '%(funcName)-20s %(message)s'),
                'log_colors': {
                    'DEBUG': 'bold_black',
                    'INFO': 'white',
                    'WARNING': 'yellow',
                    'ERROR': 'red',
                    'CRITICAL': 'bold_red',
                    'SUCCESS': 'green',
                },
            }
        },
        'handlers': {
            'console': {
                'level': CONFIG.get('level').get('console'),
                'class': 'logging.StreamHandler',
                'formatter': 'color',
            },
            'sentry': {
                'level': 'ERROR',
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
            'syslog': {
                'level': CONFIG.get('level').get('file'),
                'class': 'logging.handlers.SysLogHandler',
                'formatter': 'verbose',
                'address': (CONFIG.get('syslog').get('host'),
                            CONFIG.get('syslog').get('port'))
            },
            'file': {
                'level': CONFIG.get('level').get('file'),
                'class': 'logging.FileHandler',
                'formatter': 'verbose',
                'filename': CONFIG.get('file'),
            },
        },
        'loggers': {
            'passbook': {
                'handlers': LOG_HANDLERS,
                'level': 'DEBUG',
                'propagate': True,
            },
            'django': {
                'handlers': LOG_HANDLERS,
                'level': 'INFO',
                'propagate': True,
            },
            'tasks': {
                'handlers': LOG_HANDLERS,
                'level': 'DEBUG',
                'propagate': True,
            },
            'cherrypy': {
                'handlers': LOG_HANDLERS,
                'level': 'DEBUG',
                'propagate': True,
            },
            'oauthlib': {
                'handlers': LOG_HANDLERS,
                'level': 'DEBUG',
                'propagate': True,
            },
            'oauth2_provider': {
                'handlers': LOG_HANDLERS,
                'level': 'DEBUG',
                'propagate': True,
            },
        }
    }

_DISALLOWED_ITEMS = ['INSTALLED_APPS', 'MIDDLEWARE', 'AUTHENTICATION_BACKENDS']
# Load subapps's INSTALLED_APPS
for _app in INSTALLED_APPS:
    if _app.startswith('passbook') and \
            not _app.startswith('passbook.core'):
        if 'apps' in _app:
            _app = '.'.join(_app.split('.')[:-2])
        try:
            app_settings = importlib.import_module("%s.settings" % _app)
            INSTALLED_APPS.extend(getattr(app_settings, 'INSTALLED_APPS', []))
            MIDDLEWARE.extend(getattr(app_settings, 'MIDDLEWARE', []))
            AUTHENTICATION_BACKENDS.extend(getattr(app_settings, 'AUTHENTICATION_BACKENDS', []))
            for _attr in dir(app_settings):
                if not _attr.startswith('__') and _attr not in _DISALLOWED_ITEMS:
                    globals()[_attr] = getattr(app_settings, _attr)
        except ImportError:
            pass

if DEBUG:
    INSTALLED_APPS.append('debug_toolbar')
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
