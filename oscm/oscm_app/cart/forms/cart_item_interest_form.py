# coding=utf-8
# oscm_app/cart/forms

# django imports
from django import forms

# OSCM imports
from ..catalogue.forms.object_interest_form import ObjectInterestForm
from ..models.cart_item import CartItem


class CartItemInterestForm(ObjectInterestForm):

    """
    This class is the specific form of the OSCM Cart item details.
    """
    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = CartItem
        fields = (
            'status',
            'cart',
            'product',
            'quantity',
        )

    def __init__(self, *args, **kwargs):
        print("INIT")
        super(CartItemInterestForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['disabled'] = 'True'
        self.fields['cart'].widget.attrs['disabled'] = 'True'
        self.fields['status'].widget.attrs['disabled'] = 'True'

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        cart_item = super(forms.ModelForm, self).save(
            commit=False)
        print("CARTITEM: %s" % cart_item)
        # return self.save_product(product, commit)
        return cart_item
