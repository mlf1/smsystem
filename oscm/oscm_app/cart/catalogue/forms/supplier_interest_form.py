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
from .object_interest_form import ObjectInterestForm

# Get an instance of a logger
logger = logging.getLogger(__name__)


class SupplierInterestForm(ObjectInterestForm):

    """
    This class is the specific form of the OSCM Supplier details.
    """

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = Supplier
        fields = (
            'name',
            'address',
            'description',
            'supplier_website',
            'is_active',)

    def __init__(self, *args, **kwargs):
        is_hidden = kwargs.pop('is_hidden', None)
        super(SupplierInterestForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, [
            "name",
            "address",
            "description",
            "supplier_website",
            "is_active"])
        if is_hidden:
            self.fields['is_active'].widget = forms.HiddenInput()
            self.fields['name'].widget.attrs['readonly'] = 'True'
            self.fields['description'].widget.attrs['readonly'] = 'True'
            self.fields['address'].widget.attrs['readonly'] = 'True'
            self.fields['supplier_website'].widget.attrs['readonly'] = 'True'

    def clean_name(self):
        name = self.cleaned_data['name']
        if name != self.initial['name']:
            logger.debug("Different name")
            names = Supplier.objects.filter(
                name__iexact=name)
            if names:
                logger.error(self.error_messages['duplicate name'] % {
                    'name': name})
                raise forms.ValidationError(
                    self.error_messages['duplicate name'],
                    code='duplicate',
                    params={'name': name},)
            return name
        else:
            return self.initial['name']

    def clean_address(self):
        return self.check_update_value(
            'Supplier details',
            'address',
            self.cleaned_data['address'])

    def clean_supplier_website(self):
        return self.check_update_value(
            'Supplier details',
            'supplier_website',
            self.cleaned_data['supplier_website'])

    def clean(self):
        """
        Use a specific clean method for the current form.
        """
        # Ensures that any validation logic in parent classes is maintained.
        super(SupplierInterestForm, self).clean()
        if self._errors:
            return
        if (self.cleaned_data['name'] == self.initial['name']
                and self.cleaned_data['address'] == self.initial['address']
                and self.cleaned_data['description'] ==
                self.initial['description']
                and self.cleaned_data['supplier_website'] ==
                self.initial['supplier_website']
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
        supplier = super(forms.ModelForm, self).save(
            commit=False)
        return self.save_supplier(supplier, commit)

    def save_supplier(self, supplier, commit=True):
        """
        Save the supplier of the OSCM User if it is necessary.
        """
        if commit and self.has_been_modified:
            supplier.save()
            # Set the initial state
            self.has_been_modified = False
            logger.info(
                _(
                    "OSCM Supplier details from the supplier \'%s\' has "
                    "been updated." % supplier.name))
            return supplier
