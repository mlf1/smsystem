# oscm_app

import logging

from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _

# Get an instance of a logger
logger = logging.getLogger(__name__)


def get_attr(name, default_parameter=None):
    """
    Gets the attribute from settings file given the name.
    """
    if not hasattr(settings, name):
        if default_parameter is None:
            msg = "{error_message}: '{name}'.".format(
                error_message=_('oscm_settings_noAttribute'),
                name=name)
            logger.error(msg)
            raise ImproperlyConfigured(msg)
        else:
            return default_parameter
    else:
        return getattr(settings, name)


def next_url(request):
    """
    Returns URL to redirect to from the ``next`` param in the request.
    """
    next_page = request.REQUEST.get("next", "")
    host = request.get_host()
    return next_page if next_page and is_safe_url(
        next_page, host=host) else None


def set_form_field_order(form, fields_order):
    """
    Order the fields in the form.
    """
    assert isinstance(form.fields, OrderedDict)
    form.fields = OrderedDict(
        (f, form.fields[f]) for f in fields_order)

LOGIN_REDIRECT_URL = getattr(settings, 'LOGIN_REDIRECT_URL', '/')
USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')
PASSWORD_INPUT_RENDER_VALUE = False
SESSION_REMEMBER = None
