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
from ..forms.supplier_form import SupplierForm
from ..forms.supplier_interest_form import SupplierInterestForm
from ..models.supplier import Supplier


class SuppliersDisplay(UserCheckMixin, ListView):

    model = Supplier
    context_object_name = "suppliers"

    def get_queryset(self):
        queryset = super(SuppliersDisplay, self).get_queryset()
        if self.request.user.role == ADMIN_ROLE:
            return queryset
        else:
            return queryset.filter(is_active=True)


class SupplierDisplay(DetailView):
    context_object_name = "supplier"
    model = Supplier
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    form_class = SupplierInterestForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(SupplierDisplay, self).get_context_data(**kwargs)
        supplier = self.object
        # Add in a QuerySet of all posts for the given estimates
        context['supplier'] = supplier
        self.fill_data(supplier, context)
        if self.request.user.role == ADMIN_ROLE:
            context['products_list'] = supplier.get_products()
        else:
            context['active_products_list'] = supplier.get_active_products()
        return context

    def fill_data(self, supplier, context):
        print("Fill data in updateView")
        context['form'] = SupplierInterestForm(
            initial={
                'name': supplier.name,
                'description': supplier.description,
                'address': supplier.address,
                'supplier_website': supplier.supplier_website,
                'is_active': supplier.is_active,
            },
            is_hidden=self.request.user.role == USER_ROLE
        )


class SupplierInterest(UserCheckMixin, UpdateView):
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    form_class = SupplierInterestForm
    unsucess_template = None
    model = Supplier
    messages = {
        "supplier_details_updated": {
            "level": messages.SUCCESS,
            "text": _("OSCM Supplier details updated.")
        },
    }

    def get_context_data(self, **kwargs):
        context = super(SupplierInterest, self).get_context_data(**kwargs)
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
                self.messages['supplier_details_updated']['level'],
                self.messages['supplier_details_updated']['text'])
        return super(SupplierInterest, self).form_valid(form)

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
            'oscm:supplier',
            kwargs={'slug_name': self.kwargs['slug_name']})
        """
        return reverse('oscm:suppliers')


class AddSupplierView(UserCheckMixin, CreateView):

    model = Supplier
    template_name = "add_supplier.html"
    form_class = SupplierForm
    context_object_name = "supplier"
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"

    def get_success_url(self):
        return reverse('oscm:suppliers')


class DeleteSupplierView(UserCheckMixin, DeleteView):

    model = Supplier
    template_name = "delete_supplier.html"
    form_class = SupplierForm
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"

    def get_success_url(self):
        return reverse('oscm:suppliers')
