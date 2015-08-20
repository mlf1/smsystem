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
from .object_interest_form import ObjectInterestForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProductInterestForm(ObjectInterestForm):

    """
    This class is the specific form of the OSCM Product details.
    """

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = Product
        fields = (
            'name',
            'description',
            'unit_price',
            'quantity',
            'sku',
            'is_active',
            'category',
        )

    def __init__(self, *args, **kwargs):
        is_hidden = kwargs.pop('is_hidden', None)
        super(ProductInterestForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, [
            "name",
            "description",
            "unit_price",
            "quantity",
            "sku",
            "is_active",
            "category",
        ])
        if is_hidden:
            self.fields['is_active'].widget = forms.HiddenInput()
            self.fields['category'].widget = forms.HiddenInput()
            self.fields['name'].widget.attrs['readonly'] = 'True'
            self.fields['description'].widget.attrs['readonly'] = 'True'
            self.fields['unit_price'].widget.attrs['readonly'] = 'True'
            self.fields['quantity'].widget.attrs['readonly'] = 'True'
            self.fields['sku'].widget.attrs['readonly'] = 'True'

    def clean_name(self):
        return self.check_update_value(
            'product details',
            'name',
            self.cleaned_data['name'])

    def clean_unit_price(self):
        unit_price = self.cleaned_data['unit_price']
        if unit_price < 0:
            logger.error(self.error_messages['invalid unit price'] % {
                'unit_price': unit_price})
            raise forms.ValidationError(
                self.error_messages['invalid unit price'],
                code='invalid',
                params={'unit_price': unit_price},)
        return self.check_update_value(
            'product details',
            'unit_price',
            unit_price,
        )

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if quantity <= 0:
            logger.error(self.error_messages['invalid quantity'] % {
                'quantity': quantity})
            raise forms.ValidationError(
                self.error_messages['invalid quantity'],
                code='invalid',
                params={'quantity': quantity},)
        return self.check_update_value(
            'product details',
            'quantity',
            quantity,
        )

    def clean_sku(self):
        return self.check_update_value(
            'product details',
            'sku',
            self.cleaned_data['sku'])

    def clean(self):
        """
        Use a specific clean method for the current form.
        """
        # Ensures that any validation logic in parent classes is maintained.
        super(ProductInterestForm, self).clean()
        if self._errors:
            return
        if (self.cleaned_data['name'] == self.initial['name']
                and self.cleaned_data['description'] ==
                self.initial['description']
                and self.cleaned_data['quantity'] ==
                self.initial['quantity']
                and self.cleaned_data['sku'] ==
                self.initial['sku']
                and self.cleaned_data['unit_price'] ==
                self.initial['unit_price']
                and self.cleaned_data['is_active'] ==
                self.initial['is_active']):
            self.has_been_modified = False
            logger.debug(_("No field has been modified."))
            return
        return self.cleaned_data

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        product = super(forms.ModelForm, self).save(
            commit=False)
        return self.save_product(product, commit)

    def save_product(self, product, commit=True):
        """
        Save the product of the OSCM Product details if it is necessary.
        """
        if commit and self.has_been_modified:
            product.save()
            # Set the initial state
            self.has_been_modified = False
            logger.info(
                _(
                    "OSCM Product details from the product \'%s\' has "
                    "been updated." % product.name))
            return product
