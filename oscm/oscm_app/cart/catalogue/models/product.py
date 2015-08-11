# coding=utf-8
# oscm_app/cart/catalogue

# python imports
import uuid

# django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ...constants import PRODUCTS
from ...utils import get_attr
from ..cart_manager import CartQuerySet


def generate_product_number():
    """
    Generates the product number
    """
    return str(uuid.uuid4())


class Product(models.Model):

    """
    This class is used to represent the product.
    """

    # Supplier
    supplier = models.ForeignKey('Supplier')
    # Category
    category = models.ForeignKey('Category')
    # Creation date
    creation_date = models.DateTimeField(
        verbose_name=_('oscm_admin_creationDateOfProduct'), auto_now_add=True)
    # Last edit date
    last_edit_date = models.DateTimeField(
        verbose_name=_('oscm_admin_lastEditDateOfProduct'), auto_now=True)
    # Product name
    name = models.CharField(
        verbose_name=_('oscm_admin_nameOfProduct'),
        help_text=_('oscm_admin_helpTextNameOfProduct'),
        max_length=250,
        blank=True)
    # Slug name : part of the URL
    slug_name = models.CharField(max_length=120, unique=True, blank=False)
    # Generate product number
    # prod_no_gen = ProductNumberGenerator
    # The unique code of the product
    code = models.CharField(
        verbose_name=_('oscm_admin_codeOfProduct'),
        max_length=100,
        editable=False,
        unique=True,
        default=generate_product_number,
    )
    # Short description about the product
    description = models.TextField(
        verbose_name=_('oscm_admin_descriptionOfProduct'),
        blank=True,
        help_text=_('oscm_admin_helpTextDescriptionOfProduct')
    )
    # Unit price
    unit_price = models.DecimalField(
        verbose_name=_('oscm_admin_priceOfProduct'),
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    # Quantity
    quantity = models.PositiveIntegerField(
        verbose_name=_('oscm_admin_quantityOfProduct'),
        default=1,
    )
    #  The external unique id of the product (EAN or UPC)
    sku = models.CharField(
        verbose_name=_('oscm_admin_skuOfProduct'),
        help_text=_('oscm_admin_helpTextUniqueArticleNoOfProduct'),
        blank=True,
        max_length=30)
    # Active status, if False the product won't be displayed to shop users.
    is_active = models.BooleanField(
        verbose_name=_('oscm_admin_displayOfProduct'),
        help_text=_('oscm_admin_helpTextActiveStatusOfProduct'),
        default=False)

    class Meta:
        ordering = ["name", "category", "supplier", ]
        db_table = '%s_%s' % (get_attr('APP_NAME'), PRODUCTS)
        verbose_name = _('oscm_admin_headerOfProduct')
        verbose_name_plural = _('oscm_admin_headerOfProducts')

    objects = CartQuerySet.as_manager()

    @property
    def category_name(self):
        """
        Retrieves the category name of the product.
        """
        return self.category.name

    @property
    def supplier_name(self):
        """
        Retrieves the supplier name of the product.
        """
        return self.supplier.name

    def __str__(self):
        """
        Displays the name, the quantity and the code of products.
        """
        return _(
            "product (name: %(name)s, quantity: %(quantity)d, "
            "unit price: %(unit_price)d, code: %(code)s)") \
            % {
                'name': self.name,
                'quantity': self.quantity,
                'unit_price': self.unit_price,
                'code': self.code}
