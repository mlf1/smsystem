# coding=utf-8
# oscm_app/cart/models

# django imports
from django.db import models
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ...constants import (
    CART_ITEM_STATUSES, CART_ITEMS, DEFAULT_CART_ITEM_STATUS)
from ...utils import get_attr


class CartItem(models.Model):

    """
    This class is used to represent the cart's items.
    """

    # Default parameter for the status attribute
    DEFAULT_CART_ITEM_STATUS = get_attr(DEFAULT_CART_ITEM_STATUS)
    # Retrieved the different statuses from the settings file
    CART_ITEM_STATUSES = get_attr(CART_ITEM_STATUSES)
    # Status
    status = models.CharField(
        verbose_name=_('oscm_admin_statusOfCartItem'),
        max_length=32,
        default=DEFAULT_CART_ITEM_STATUS,
        choices=CART_ITEM_STATUSES,
        help_text=_('oscm_admin_helpTextStatusOfCartItem'),
    )
    # Product
    product = models.ForeignKey('Product')
    # Cart
    cart = models.ForeignKey('Cart', null=True, blank=True)
    # Quantity
    quantity = models.PositiveIntegerField(
        verbose_name=_('oscm_admin_quantityOfCartItem'),
        default=1,
    )
    # Total price
    total_price = models.DecimalField(
        verbose_name=_('oscm_admin_totalPriceOfCartItem'),
        max_digits=8,
        decimal_places=2,
        default=0,
    )
    # Creation date
    creation_date = models.DateTimeField(
        verbose_name=_('oscm_admin_creationDateOfCartItem'),
        auto_now_add=True,
    )
    # Last edit date
    last_edit_date = models.DateTimeField(
        verbose_name=_('oscm_admin_lastEditDateOfCartItem'),
        auto_now=True,
    )

    class Meta:
        ordering = ["status", "creation_date", ]
        db_table = '%s_%s' % (get_attr('APP_NAME'), CART_ITEMS)
        verbose_name = _('oscm_admin_headerOfCartItem')
        verbose_name_plural = _('oscm_admin_headerOfCartItems')

    @property
    def name(self):
        """
        Retrieves the name of cart item.
        """
        return self.product.name

    @property
    def total_price(self):
        """
        Retrieves the total price of cart item.
        """
        return self.product.unit_price*self.quantity

    def get_absolute_url(self):
        """
        """
        return self.product.get_absolute_url()

    def __str__(self):
        """
        Displays the cart id and the product name or
        the product name and the item status.
        """
        if self.cart:
            return '{0}: {1}'.format(self.cart.id, self.product.name)
        else:
            return '{0}: {1}'.format(self.product.name, self.status)
