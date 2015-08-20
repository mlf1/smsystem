# coding=utf-8
# oscm_app/cart/catalogue/forms

# python imports
import logging

# django imports
from django import forms
from django.utils.translation import ugettext as _

# OSCM imports
from ....utils import set_form_field_order
from ..models.supplier import Supplier

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SupplierForm(forms.ModelForm):

    """
    This class is the specific form of the OSCM Category.
    """

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = Supplier
        fields = (
            "name",
            "address",
            "description",
            "supplier_website",
            "is_active",
        )

    def __init__(self, *args, **kwargs):
        super(SupplierForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, [
            "name",
            "address",
            "description",
            "supplier_website",
            "is_active"])

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        supplier = super(forms.ModelForm, self).save(
            commit=False)
        return self.save_supplier(supplier, commit)

    def save_supplier(self, supplier, commit=True):
        """
        Save the supplier of the OSCM User if it is necessary.
        """
        if commit:
            supplier.save()
            logger.info(
                _(
                    "OSCM Supplier \'%s\' has "
                    "been created." % supplier.name))
            return supplier
