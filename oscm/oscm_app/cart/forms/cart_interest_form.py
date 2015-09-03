# coding=utf-8
# oscm_app/cart/forms

# python imports
import datetime
import logging

# django imports
from django import forms
from django.forms.extras.widgets import SelectDateWidget
# from django.forms import SplitDateTimeWidget
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ...constants import DEFAULT_CART_STATUS
from ...utils import get_attr, set_form_field_order
from ..catalogue.forms.object_interest_form import ObjectInterestForm
from ..models.cart import Cart

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CartInterestForm(ObjectInterestForm):

    """
    This class is the specific form of the OSCM Cart details.
    """

    nb_cart_items = forms.IntegerField(
        min_value=0,
        label=_('oscm_admin_nbCartItemsLabelOfCart'),
        widget=forms.TextInput(),)
    total_amount = forms.IntegerField(
        min_value=0,
        label=_('oscm_admin_totalAmountLabelOfCart'),
        widget=forms.TextInput(),)

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = Cart
        fields = (
            'project_name',
            'description',
            'owner',
            'requested_due_date',
            'status',
            'nb_cart_items',
            'total_amount',
        )
        widgets = {
            'requested_due_date': SelectDateWidget(), }
        is_hidden = False

    def __init__(self, *args, **kwargs):
        self.is_hidden = kwargs.pop('is_hidden', None)
        super(CartInterestForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, [
            "project_name",
            "description",
            "owner",
            "requested_due_date",
            "status",
            "nb_cart_items",
            "total_amount"])
        if self.is_hidden:
            self.fields['owner'].widget = forms.HiddenInput()
            # Form isn't editable for the user (role=U)
            # and cart.status=completed or saved)
            if self.initial['status'] != get_attr(DEFAULT_CART_STATUS):
                self.fields['project_name'].widget.attrs['readonly'] = 'True'
                self.fields['description'].widget.attrs['readonly'] = 'True'
                self.fields['requested_due_date'].widget.attrs[
                    'disabled'] = 'True'
        # Show 'status' and 'nb_cart_items', but these fields aren't editable.
        self.fields['status'].widget.attrs['disabled'] = 'True'
        self.fields['status'].required = False
        self.fields['nb_cart_items'].widget.attrs['readonly'] = 'True'
        self.fields['total_amount'].widget.attrs['readonly'] = 'True'

    def clean_project_name(self):
        return self.check_update_value(
            'cart details',
            'project_name',
            self.cleaned_data['project_name'])

    def clean_owner(self):
        return self.check_update_value(
            'cart details',
            'owner',
            self.cleaned_data['owner'])

    def clean_requested_due_date(self):
        if 'requested_due_date' in self.cleaned_data.keys():
            requested_due_date = self.cleaned_data['requested_due_date']
            if requested_due_date.date() < datetime.date.today():
                """
                self.errors.append(forms.ValidationError(
                "La date doit être postérieure à la date actuelle"))
                """
                logger.error(self.error_messages['wrong date'] % {
                    'requested_due_date': requested_due_date.date(),
                    'today': datetime.date.today()})
                raise forms.ValidationError(
                    self.error_messages['wrong date'],
                    code='wrong',
                    params={
                        'requested_due_date': requested_due_date.date(),
                        'today': datetime.date.today()},)
            else:
                return self.check_update_value(
                    'cart details',
                    'requested_due_date',
                    self.cleaned_data['requested_due_date'])
        else:
            requested_due_date = None
            logger.error(self.error_messages['invalid date'] % {
                'date': requested_due_date})
            raise forms.ValidationError(
                self.error_messages['invalid date'],
                code='invalid',
                params={'date': requested_due_date},)

    def clean_status(self):
        return self.instance.status

    def clean(self):
        """
        Use a specific clean method for the current form.
        """
        # Ensures that any validation logic in parent classes is maintained.
        super(CartInterestForm, self).clean()
        if self._errors:
            return
        if (self.cleaned_data['project_name'] == self.initial['project_name']
                and self.cleaned_data['description'] ==
                self.initial['description']
                and self.cleaned_data['owner'] == self.initial['owner']
                and self.cleaned_data['requested_due_date'] ==
                self.initial['requested_due_date']):
            self.has_been_modified = False
            logger.debug(_("No field has been modified."))
            return
        return self.cleaned_data

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        cart = super(forms.ModelForm, self).save(
            commit=False)
        return self.save_cart(cart, commit)

    def save_cart(self, cart, commit=True):
        """
        Save the cart of the OSCM User if it is necessary.
        """
        if commit and self.has_been_modified:
            cart.save()
            # Set the initial state
            self.has_been_modified = False
            logger.info(
                _(
                    "OSCM Cart details from the cart \'%s\' has "
                    "been updated." % cart.project_name))
            return cart
