# coding=utf-8
# oscm_app/cart/views

# django imports
from django.shortcuts import get_object_or_404

# django import
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    UpdateView
)

# OSCM imports
from ...constants import CART_ITEM_STATUSES, DEFAULT_CART_ITEM_STATUS
from ...decorators.user_check_mixin import UserCheckMixin
from ...utils import get_attr
from ..catalogue.models.product import Product
from ..forms.cart_item_interest_form import CartItemInterestForm
from ..models.cart import Cart
from ..models.cart_item import CartItem


class CartItemDisplay(DetailView):

    context_object_name = "cart_item"
    model = CartItem
    form_class = CartItemInterestForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CartItemDisplay, self).get_context_data(**kwargs)
        cart_item = self.object
        # Add in a QuerySet of all posts for the given estimates
        context['cart_item'] = cart_item
        self.fill_data(cart_item, context)
        return context

    def fill_data(self, cart_item, context):
        print("FILL CONTEXT FORM")
        context['form'] = CartItemInterestForm(
            initial={
                'status': cart_item.status,
                'cart': cart_item.cart,
                'product': cart_item.product,
                'quantity': cart_item.quantity,
                'total_price': cart_item.total_price,
            },)


class CartItemInterest(UserCheckMixin, UpdateView):

    pk_url_kwarg = "pk"
    form_class = CartItemInterestForm
    model = CartItem
    unsucess_template = None
    messages = {
        "cart_item_details_updated": {
            "level": messages.SUCCESS,
            "text": _("OSCM Cart item details updated.")
        },
    }

    def get_context_data(self, **kwargs):
        context = super(CartItemInterest, self).get_context_data(**kwargs)
        context['pk'] = self.kwargs['pk']
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        instance = form.save()
        if instance:
            messages.add_message(
                self.request,
                self.messages['cart_item_details_updated']['level'],
                self.messages['cart_item_details_updated']['text'])
        return super(CartItemInterest, self).form_valid(form)

    def form_invalid(self, form):
        """
        This is what's called when the form is invalid.
        """
        if self.unsucess_template:
            self.template_name = self.unsucess_template
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse(
            'oscm:cart_item',
            kwargs={'pk': self.kwargs['pk']})


class AddCartItemView(UserCheckMixin, CreateView):

    model = CartItem
    template_name = "add_cart_item.html"
    form_class = CartItemInterestForm
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"

    def get_initial(self):
        initial = super(AddCartItemView, self).get_initial()
        initial['slug_name'] = self.kwargs.get('slug_name')
        initial['product'] = get_object_or_404(
            Product,
            slug_name=self.kwargs.get('slug_name'))
        # initial['cart'] = Cart.objects.filter(owner=self.request.user)
        initial['cart'] = get_object_or_404(
            Cart,
            owner=self.request.user)
        initial['status'] = get_attr(
            CART_ITEM_STATUSES)[get_attr(DEFAULT_CART_ITEM_STATUS)]
        initial['user'] = self.request.user
        print("Initial_ci: %s" % initial)
        return initial

    def get_context_data(self, **kwargs):
        context = super(AddCartItemView, self).get_context_data(**kwargs)
        # Use with url parameters
        context['slug_name'] = kwargs.get('slug_name')
        print("CONTEXT: %s" % kwargs)
        return context

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AddCartItemView, self).get_form_kwargs(**kwargs)
        kwargs['initial']['user'] = self.request.user
        # kwargs['initial']['product'] = get_object_or_404(
        # Product, slug_name=self.kwargs.get('slug_name'))
        # Use for fill the form
        kwargs['initial']['slug_name'] = self.kwargs.get('slug_name')
        print("KWARGS_ : %s" % kwargs)
        if 'data' in kwargs:
            print("KWARGS KWARGS: %s" % kwargs)
        return kwargs

    def form_valid(self, form):
        print("VALID FORM")
        return super(AddCartItemView, self).form_valid(form)

    def form_invalid(self, form):
        print("INVALID FORM")
        return super(AddCartItemView, self).form_invalid(form)

    def get_success_url(self):
        return reverse('oscm:carts')


class DeleteCartItemView(UserCheckMixin, DeleteView):

    model = CartItem
    template_name = "delete_cart_item.html"
    form_class = CartItemInterestForm
    context_object_name = 'cart_item'
    pk_url_kwarg = "pk"

    def get_success_url(self):
        return reverse('oscm:carts', kwargs={'pk': self.object.cart.owner.id})
