# coding=utf-8
# oscm_app/cart/supplier

# django imports
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ...constants import SUPPLIERS
from ...utils import get_attr
from ..cart_manager import CartQuerySet
from .product import Product


class Supplier(models.Model):

    """
    This class is used to represent the supplier.
    * A supplier holds all shop supplier related information.
    * A Supplier is only created by the OSCM administrator.
    """
    products = models.ManyToManyField(
        'Product',
        through='Offre',
        related_name='suppliers')
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
        return Product.objects.filter(supplier=self)

    def get_absolute_url(self):
        """
        Retrieves the specific url of the supplier.
        """
        return reverse(
            'oscm:supplier_view',
            kwargs={'supplier_slug': self.slug_name})

    def __str__(self):
        """
        Displays the name and the creation date.
        """
        return '{0}: {1}'.format(self.name, self.creation_date)


class Offre(models.Model):

    """
    This class is used as an intermediary class between
    'Product' and 'Supplier'
    """
    product = models.ForeignKey('Product')
    supplier = models.ForeignKey('Supplier')

    class Meta:
        unique_together = ('product', 'supplier')

    def __str__(self):
        return "{0} sent by {1}".format(self.product, self.supplier)
