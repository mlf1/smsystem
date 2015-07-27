# coding=utf-8
# oscm_app

# python imports
import logging
import uuid
from collections import OrderedDict

# django imports
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.http import is_safe_url
from django.utils.translation import ugettext as _

# OSCM imports
from .constants import ORDER_BASE

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


class OrderNumberGenerator(object):

    """
    Simple object for generating order numbers.
    We need this as the order number is required for invoice
    which takes place before the order model has been created.
    """

    # No order
    no_order = 0

    def generate_order_number(self, cart):
        """
        Return a new order number for a given cart.
        """
        self.no_order = ORDER_BASE + cart.id
        return str(self.no_order)

    def __str__(self):
        """
        Displays the new order number.
        """
        return 'No order: {0}'.format(self.no_order)


class ProductNumberGenerator(object):

    """
    Simple object for generating product numbers.
    """

    # No prod
    no_prod = 0

    def generate_product_number(self):
        """
        Return a new product number.
        """
        self.no_prod = uuid.uuid4()
        return str(self.no_prod)

    def __str__(self):
        """
        Displays the new product number.
        """
        return 'No product: {0}'.format(self.no_prod)
