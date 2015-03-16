# oscm_app

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext as _


def get_attr(name):
    """
    Gets the attribute from settings file given the name.
    """
    if not hasattr(settings, name):
        raise ImproperlyConfigured("{error_message}: '{name}'.".format(
            error_message=_('oscm_settings_noAttribute'),
            name=name))
    else:
        return getattr(settings, name)
