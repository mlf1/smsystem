"""
Django settings for oscm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import logging.config
import os
from django.utils.translation import ugettext_lazy
from django.conf import global_settings as default_settings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

APP_NAME = 'oscm_app'
APP_CORE = 'core'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'njlzn&@v=wse614vybnntrrr+tj#9xj7*!w_$wcez^se5y1!v$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    APP_NAME,
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'oscm_system.urls'

WSGI_APPLICATION = 'oscm_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {'init_command': 'SET foreign_key_checks = 0;' },
        'NAME': 'oscm_db',
        'USER': 'root',
        'PASSWORD': 'bfh',
        'HOST': '127.0.0.1',
        'PORT': '',
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

# Default language, it will be used, if django can't recognize user's language
LANGUAGE_CODE = 'en'

# List of activated languages
LANGUAGES = (
    ('de', ugettext_lazy('German')),
    ('en', ugettext_lazy('English')),
    ('fr', ugettext_lazy('French')),
)

TIME_ZONE = 'Europe/Zurich'

# Enable django’s translation system
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = os.path.join(BASE_DIR, 'static/')

ROOT_PATH = os.path.join(BASE_DIR, '..')

STATIC_ROOT = os.path.join(ROOT_PATH, 'static')

# Additional locations of static files
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, APP_NAME, APP_CORE, 'static'),
)

# Used for the translation files
LOCALE_PATHS = (
    os.path.join(BASE_DIR, APP_NAME, APP_CORE, 'locale'),
)

# Additional locations of templates files
TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, APP_NAME, APP_CORE, 'templates'),
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

############################
#      OSCM settings       #
############################
# Authentication User Model
AUTH_USER_MODEL = '{0}.{1}'.format(APP_NAME, 'CustomAuthUser')

# Default role
DEFAULT_ROLE = 'U'

# User roles
USER_ROLES = (
    ('U', 'User'),
    ('M', 'Manager'),
    ('A', 'Admin'),
)

# Default authentication mode
DEFAULT_AUTHENTICATION_MODE = 'D'

# User authentication modes
USER_AUTHENTICATION_MODES = (
    ('D', 'Django'),
    # The following feature doesn't yet exist. Ex: ('L', 'Ldap'),
)

# Used for the authentication in the frontend
LOGIN_URL = 'oscm:login'
LOGOUT_URL = 'oscm:logout'
LOGIN_REDIRECT_URL = 'oscm:index'

# Used to keep the session active for longer periods of time
SESSION_REMEMBER = None
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 3

# Used with the registration process in the frontend
# If True, users can register
REGISTRATION_OPEN = True

# If True, the user's account will be automatically activated.
REGISTRATION_AUTO_ACTIVATED_ACCOUNT = False

TEMPLATE_CONTEXT_PROCESSORS = default_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'oscm_app.custom_context_processors.retrieve_setting_parameters',
    'django.core.context_processors.request',
)

# Logging configuration.
LOGGING_CONFIG = None
# Date format of logs.
LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# Base directory of logs.
LOG_BASE_DIR = os.path.normpath(os.path.join(BASE_DIR, 'logs'))
# Max size of rotating files (bytes).
LOG_MAX_SIZE = 1024 * 1024 * 5
# Count of backup files for the logs (=how many rollovers are kept).
LOG_BACKUP_COUNT = 7
# Whatever I want, as I already have
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format':
                '[%(asctime)s] %(levelname)s %(module)s '
                '%(message)s',
            'datefmt': LOG_DATE_FORMAT,
            },
        'main_formatters': {
            'format':
                '%(levelname)s:%(name)s: %(message)s '
                '(%(asctime)s; %(filename)s:%(lineno)d)',
            'datefmt': LOG_DATE_FORMAT,
            },
        'verbose': {
            'format':
                "[%(asctime)-15s] %(name)-5s %(levelname)-8s "
                "(%(filename)s:%(lineno)d) "
                "%(message)s",
            'datefmt': LOG_DATE_FORMAT,
            },
        'full_verbose': {
            'format':
                '[LEVEL:%(levelname)s] TIME:%(asctime)s '
                '[MODULE:%(module)s FUNCNAME:%(funcName)s LINE:%(lineno)d] '
                'PROCESS:%(process)d THREAD:%(thread)d MESSAGE:%(message)s',
            'datefmt': LOG_DATE_FORMAT,
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'oscm_app': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(
                LOG_BASE_DIR,
                'oscm_app.log'),
            'formatter': 'simple',
            'filters': ['require_debug_false'],
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            # 'stream': sys.stdout
            'filters': ['require_debug_true'],
            'formatter': 'main_formatters',
        },
        'test': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(
                LOG_BASE_DIR,
                'main_debug.log'),
            # 5 MB
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'full_verbose',
            'filters': ['require_debug_true'],
        },
        'prod': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(
                LOG_BASE_DIR,
                'main.log'),
            # 5 MB
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'main_formatters',
            'filters': ['require_debug_false'],
        },
        'dba_logfile': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(
                LOG_BASE_DIR,
                'django_dba.log'),
            # 5 MB
            'maxBytes': LOG_MAX_SIZE,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'simple'
        },
        'null': {
            "class": 'django.utils.log.NullHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['null'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['mail_admins', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django.db.backends': {
            'handlers': ['dba_logfile', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'oscm_app': {
            'handlers': ['oscm_app', 'test', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['null'],
        },
        '': {
            'handlers': ['console', 'prod', 'test'],
            'level': 'DEBUG',
        },
    }
}

logging.config.dictConfig(LOGGING)
