# coding=utf-8
# oscm_app

# python imports
import logging

# django imports
from django.contrib import messages
from django.db.models.signals import post_delete
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from oscm_app.cart.models.cart_item import CartItem
from oscm_app.cart.catalogue.models.category import Category
from oscm_app.cart.catalogue.models.product import Product
from oscm_app.cart.catalogue.models.supplier import Supplier
from oscm_app.constants import (
    CART_ITEM_DELETED_SIGNAL,
    CATEGORY_DELETED_SIGNAL,
    CATEGORY_UPDATED_SIGNAL,
    PRODUCT_DELETED_SIGNAL,
    SUPPLIER_DELETED_SIGNAL
)
from oscm_app.signals import category_updated

# Get an instance of a logger
logger = logging.getLogger(__name__)

message_details = {
    "category_deleted": {
        "level": messages.SUCCESS,
        "text": _("OSCM Category deleted.")
    },
    "product_deleted": {
        "level": messages.SUCCESS,
        "text": _("OSCM Product deleted.")
    },
    "supplier_deleted": {
        "level": messages.SUCCESS,
        "text": _("OSCM Supplier deleted.")
    },
}


def category_updated_handler(sender, **kwargs):
    """
    Signal intercept for category updated
    """
    category = kwargs['category']
    form = kwargs['form']
    print("I\'ve received the signal for the category %s "
          "from the form %s" % (category, form))


def category_deleted_handler(sender, **kwargs):
    """
    Signal intercept for category deleted
    """
    if kwargs.get('instance'):
        logger.info(
            _("OSCM Category \'%s\' has been "
              "deleted." % kwargs['instance'].name))


def product_deleted_handler(sender, **kwargs):
    """
    Signal intercept for product deleted
    """
    if kwargs.get('instance'):
        logger.info(
            _("OSCM Product \'%s\' has been "
              "deleted." % kwargs['instance'].name))


def supplier_deleted_handler(sender, **kwargs):
    """
    Signal intercept for supplier deleted
    """
    if kwargs.get('instance'):
        logger.info(
            _("OSCM Supplier \'%s\' has been "
              "deleted." % kwargs['instance'].name))


def cart_item_deleted_handler(sender, **kwargs):
    """
    Signal intercept for cart_item deleted
    """
    if kwargs.get('instance'):
        logger.info(
            _("OSCM Cart Item \'%s\' has been "
              "deleted." % kwargs['instance'].name))

# Connect for OSCM Category model
category_updated.connect(
    category_updated_handler, dispatch_uid=CATEGORY_UPDATED_SIGNAL)
post_delete.connect(
    category_deleted_handler,
    sender=Category,
    dispatch_uid=CATEGORY_DELETED_SIGNAL)

# Connect for OSCM Product model
post_delete.connect(
    product_deleted_handler,
    sender=Product,
    dispatch_uid=PRODUCT_DELETED_SIGNAL)

# Connect for OSCM Supplier
post_delete.connect(
    supplier_deleted_handler,
    sender=Supplier,
    dispatch_uid=SUPPLIER_DELETED_SIGNAL)

# Connect for OSCM Cart Item
post_delete.connect(
    cart_item_deleted_handler,
    sender=CartItem,
    dispatch_uid=CART_ITEM_DELETED_SIGNAL)
