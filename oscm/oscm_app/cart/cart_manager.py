# coding=utf-8
# oscm_app/cart

# django imports
from django.db.models import Manager


class CartManager(Manager):

    """
    This class is used to represent the cart manager.
    """

    def active(self):
        """
        Retrieve model with active status.
        """
        return self.filter(is_active=True)
