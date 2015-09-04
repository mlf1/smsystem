# coding=utf-8
# oscm_app/cart

# django imports
from django.db import models


class CartQuerySet(models.QuerySet):

    """
    This class is used to represent the cart querySet.
    """

    def active(self):
        return self.filter(is_active=True)


class CartManager(models.Manager):

    """
    This class is used to represent the cart manager.
    """

    def active(self):
        """
        Retrieve model with active status.
        """
        return self.filter(is_active=True)
