# coding=utf-8
# oscm_app/cart

# django import
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView, ListView, UpdateView

# OSCM imports
from ..constants import (
    ADMIN_ROLE,
    MANAGER_ROLE,
    USER_ROLE)
from ..decorators.user_check_mixin import UserCheckMixin
from .forms.cart_interest_form import CartInterestForm
from .models.cart import Cart


class CartDisplay(DetailView):

    context_object_name = "cart"
    model = Cart
    form_class = CartInterestForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(CartDisplay, self).get_context_data(**kwargs)
        cart = self.object
        # Add in a QuerySet of all posts for the given estimates
        context['cart'] = cart
        context['cart_items_list'] = cart.get_cart_items()
        self.fill_data(cart, context)
        return context

    def fill_data(self, cart, context):
        context['form'] = CartInterestForm(
            initial={
                'project_name': cart.project_name,
                'description': cart.description,
                'owner': cart.owner,
                'requested_due_date': cart.requested_due_date,
                'status': cart.status,
                'nb_cart_items': cart.nb_cart_items,
            },
            is_hidden=self.request.user.role == USER_ROLE
        )


class CartsDisplay(UserCheckMixin, ListView):

    context_object_name = "carts"
    model = Cart

    def get_queryset(self):
        """
        List OSCM Carts for a specific user role.
        """
        # self.args[0] suppose que l'url prend un paramètre, ce que nous
        # n'avons pas fait.  C'est pour l'exemple.
        queryset = super(CartsDisplay, self).get_queryset()
        if self.request.user.role == \
                MANAGER_ROLE or self.request.user.role == ADMIN_ROLE:
            # return Cart.objects.all()
            return queryset
        elif self.request.user.role == USER_ROLE:
            # return Cart.objects.filter(owner=self.request.user)
            return queryset.filter(owner=self.request.user)
        else:
            return


class CartInterest(UserCheckMixin, UpdateView):

    form_class = CartInterestForm
    model = Cart
    unsucess_template = None
    messages = {
        "cart_details_updated": {
            "level": messages.SUCCESS,
            "text": _("OSCM Cart details updated.")
        },
    }

    def get_context_data(self, **kwargs):
        context = super(CartInterest, self).get_context_data(**kwargs)
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
                self.messages['cart_details_updated']['level'],
                self.messages['cart_details_updated']['text'])
        return super(CartInterest, self).form_valid(form)

    def form_invalid(self, form):
        """
        This is what's called when the form is invalid.
        """
        if self.unsucess_template:
            self.template_name = self.unsucess_template
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse(
            'oscm:cart',
            kwargs={'pk': self.kwargs['pk']})
