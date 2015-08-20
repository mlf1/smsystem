# coding=utf-8
# oscm_app/cart/catalogue/forms

# python imports
import logging

# django imports
from django import forms
from django.utils.translation import ugettext as _

# OSCM imports
from ....utils import set_form_field_order
from ..models.product import Product

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProductForm(forms.ModelForm):

    """
    This class is the specific form of the OSCM Category.
    """

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = Product
        fields = (
            "name",
            "description",
            "unit_price",
            "quantity",
            "sku",
            "is_active",
            "category",
        )

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, [
            "name",
            "description",
            "unit_price",
            "quantity",
            "sku",
            "is_active",
            "category", ])

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        product = super(forms.ModelForm, self).save(
            commit=False)
        return self.save_product(product, commit)

    def save_product(self, product, commit=True):
        """
        Save the product of the OSCM User if it is necessary.
        """
        if commit:
            product.save()
            logger.info(
                _(
                    "OSCM Product \'%s\' has "
                    "been created." % product.name))
            return product
