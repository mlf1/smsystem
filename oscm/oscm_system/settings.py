"""
Django settings for oscm project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
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
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'oscm_db.sqlite3'),
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

STATIC_URL = '/static/'

STATIC_ROOT = '/Users/mlf/Projets/myRepo/smsystem/oscm/static'

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
