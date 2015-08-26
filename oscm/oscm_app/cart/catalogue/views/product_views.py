# coding=utf-8
# oscm_app/cart/catalogue/views

# python imports
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView
)
# OSCM imports
from ....constants import (ADMIN_ROLE, USER_ROLE)
from ....decorators.user_check_mixin import UserCheckMixin
from ..forms.product_form import ProductForm
from ..forms.product_interest_form import ProductInterestForm
from ..models.product import Product


class ProductsDisplay(UserCheckMixin, ListView):

    model = Product
    context_object_name = "products"

    def get_queryset(self):
        queryset = super(ProductsDisplay, self).get_queryset()
        if self.request.user.role == ADMIN_ROLE:
            return queryset
        else:
            return queryset.filter(is_active=True)


class ProductInterest(UserCheckMixin, UpdateView):

    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    form_class = ProductInterestForm
    unsucess_template = None
    model = Product
    messages = {
        "product_details_updated": {
            "level": messages.SUCCESS,
            "text": _("OSCM Product details updated.")
        },
    }

    def get_context_data(self, **kwargs):
        context = super(ProductInterest, self).get_context_data(**kwargs)
        context['slug_name'] = self.kwargs['slug_name']
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        instance = form.save()
        if instance:
            messages.add_message(
                self.request,
                self.messages['product_details_updated']['level'],
                self.messages['product_details_updated']['text'])
        return super(ProductInterest, self).form_valid(form)

    def form_invalid(self, form):
        """
        This is what's called when the form is invalid.
        """
        if self.unsucess_template:
            self.template_name = self.unsucess_template
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        """
        return reverse(
            'oscm:product',
            kwargs={'slug_name': self.kwargs['slug_name']})
        """
        return reverse('oscm:products')


class ProductDisplay(DetailView):

    context_object_name = "product"
    model = Product
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    form_class = ProductInterestForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(ProductDisplay, self).get_context_data(**kwargs)
        product = self.object
        # Add in a QuerySet of all posts for the given estimates
        context['product'] = product
        self.fill_data(product, context)
        if self.request.user.role == ADMIN_ROLE:
            context['suppliers_list'] = product.get_suppliers()
        else:
            context['active_suppliers_list'] = product.get_active_suppliers()
        return context

    def fill_data(self, product, context):
        context['form'] = ProductInterestForm(
            initial={
                'name': product.name,
                'description': product.description,
                'unit_price': product.unit_price,
                'quantity': product.quantity,
                'minimum_quantity': product.minimum_quantity,
                'sku': product.sku,
                'is_active': product.is_active,
                'category': product.category,
            },
            is_hidden=self.request.user.role == USER_ROLE
        )


class AddProductView(UserCheckMixin, CreateView):

    model = Product
    template_name = "add_product.html"
    form_class = ProductForm
    context_object_name = "product"
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    messages = {
        "product_created": {
            "level": messages.SUCCESS,
            "text": _("OSCM Product created.")
        },
    }

    def form_valid(self, form):
        instance = form.save()
        if instance:
            messages.add_message(
                self.request,
                self.messages['product_created']['level'],
                self.messages['product_created']['text'])
        return super(AddProductView, self).form_valid(form)

    def get_success_url(self):
        return reverse('oscm:products')


class DeleteProductView(UserCheckMixin, DeleteView):

    model = Product
    template_name = "delete_product.html"
    form_class = ProductForm
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"

    def get_success_url(self):
        return reverse('oscm:products')
