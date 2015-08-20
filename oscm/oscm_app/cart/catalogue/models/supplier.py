# coding=utf-8
# oscm_app/cart/supplier/models

# python imports
import re

# django imports
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.db import models
from django.utils.encoding import force_text
from django.utils.six.moves.urllib.parse import urlsplit, urlunsplit
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ....constants import SUPPLIERS
from ....utils import get_attr
from ...cart_manager import CartQuerySet


class URLValidator(RegexValidator):
    """
    This validator allows underscores within the subdomains of URLS
    """
    regex = re.compile(
        # http:// or https://
        r'^(?:http)s?://'
        # Subdomain that allow underscores
        r'(?:(?:(?:[A-Z0-9](?:[A-Z0-9-_]{0,61}[A-Z0-9])?\.)?'
        # domain
        r'(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?'
        '|[A-Z0-9-]{2,}(?<!-)\.))|'
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    message = _('Enter a valid URL')

    def __call__(self, value):
        try:
            super(URLValidator, self).__call__(value)
        except ValidationError as e:
            # Trivial case failed. Try for possible IDN domain
            if value:
                value = force_text(value)
                scheme, netloc, path, query, fragment = urlsplit(value)
                try:
                    # IDN -> ACE
                    netloc = netloc.encode('idna').decode('ascii')
                except UnicodeError:  # invalid domain part
                    raise e
                url = urlunsplit((scheme, netloc, path, query, fragment))
                super(URLValidator, self).__call__(url)
            else:
                raise
        else:
            url = value


class Supplier(models.Model):

    """
    This class is used to represent the supplier.
    * A supplier holds all shop supplier related information.
    * A Supplier is only created by the OSCM administrator.
    """
    products = models.ManyToManyField(
        'Product')
    # through='Offre',
    # related_name='suppliers')
    # Supplier name
    name = models.CharField(
        max_length=250,
        null=False,
        blank=False,
        unique=True)
    # Slug name : part of the URL
    slug_name = models.SlugField(max_length=120, unique=True, blank=False)
    # Short description about the supplier
    description = models.TextField(
        verbose_name=_("oscm_admin_descriptionOfSupplier"),
        blank=True,
        help_text=_('oscm_admin_helpTextDescriptionOfSupplier')
    )
    # Creation date
    creation_date = models.DateTimeField(
        verbose_name=_('oscm_admin_creationDateOfSupplier'), auto_now_add=True)
    # Last edit date
    last_edit_date = models.DateTimeField(
        verbose_name=_('oscm_admin_lastEditDateOfSupplier'), auto_now=True)
    # Supplier address
    address = models.CharField(verbose_name=_('oscm_admin_addressOfSupplier'),
                               max_length=80)
    # Supplier website
    supplier_website = models.URLField(
        verbose_name=_('oscm_admin_websiteOfSupplier'),
        max_length=100,
        blank=True,
        null=True,
        help_text=_("Url must start with \'http://\' or \'https://\'."),
        validators=[URLValidator()])
    # Active status
    is_active = models.BooleanField(
        verbose_name=_('oscm_admin_activeStatusOfSupplier'),
        default=False,
        null=False,
        help_text=_('oscm_admin_helpTextActiveStatusOfSupplier'))

    class Meta:
        ordering = ["name", ]
        db_table = '%s_%s' % (get_attr('APP_NAME'), SUPPLIERS)
        verbose_name = _('oscm_admin_headerOfSupplier')
        verbose_name_plural = _('oscm_admin_headerOfSuppliers')

    objects = CartQuerySet.as_manager()

    def get_products(self):
        """
        Retrieves all products from the current supplier.
        """
        return Supplier.objects.get(id=self.id).products.all()

    def get_active_products(self):
        """
        Retrieves all active products from the current supplier.
        """
        return Supplier.objects.get(id=self.id).products.filter(is_active=True)

    def get_absolute_url(self):
        """
        Retrieves the specific url of the supplier.
        """
        return reverse(
            'oscm:supplier_view',
            kwargs={'supplier_slug': self.slug_name})

    def __str__(self):
        """
        Displays the name and the address.
        """
        return _(
            "supplier (name: %(name)s, address: %(address)s)") \
            % {
                'name': self.name,
                'address': self.address,
                'is_active': self.is_active, }

    def get_delete_url(self):
        return reverse(
            'oscm:delete_supplier',
            kwargs={'slug_name': self.slug_name})

    def save(self, *args, **kwargs):
        """
        Saves supplier with the slug parameter.
        """
        self.slug_name = slugify(self.name)
        super(Supplier, self).save(*args, **kwargs)

"""
class Offre(models.Model):

    ""
    This class is used as an intermediary class between
    'Product' and 'Supplier'
    ""
    product = models.ForeignKey('Product')
    supplier = models.ForeignKey('Supplier')

    class Meta:
        unique_together = ('product', 'supplier')

    def __str__(self):
        return "{0} sent by {1}".format(self.product, self.supplier)
"""
