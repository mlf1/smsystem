# coding=utf-8
# oscm_app/cart/catalogue/views

# django imports
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
from ..forms.category_form import CategoryForm
from ..forms.category_interest_form import CategoryInterestForm
from ..models.category import Category
# from oscm_app import signals


class CategoriesDisplay(UserCheckMixin, ListView):

    model = Category
    context_object_name = "categories"

    def get_queryset(self):
        queryset = super(CategoriesDisplay, self).get_queryset()
        if self.request.user.role == ADMIN_ROLE:
            return queryset
        else:
            return queryset.filter(is_active=True)


class CategoryInterest(UserCheckMixin, UpdateView):

    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    form_class = CategoryInterestForm
    unsucess_template = None
    model = Category
    messages = {
        "category_details_updated": {
            "level": messages.SUCCESS,
            "text": _("OSCM Category details updated.")
        },
    }

    def get_context_data(self, **kwargs):
        context = super(CategoryInterest, self).get_context_data(**kwargs)
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
                self.messages['category_details_updated']['level'],
                self.messages['category_details_updated']['text'])
            """
            signals.category_updated.send(
                sender=CategoryInterestForm,
                category=instance,
                form=form)
            """
        return super(CategoryInterest, self).form_valid(form)

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
            'oscm:category',
            kwargs={'slug_name': self.kwargs['slug_name']})
        """
        return reverse('oscm:categories')


class CategoryDisplay(DetailView):

    context_object_name = "category"
    model = Category
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"
    form_class = CategoryInterestForm

    """
    def get_form_kwargs(self, **kwargs):
        kwargs = super(CategoryDisplay, self).get_form_kwargs(**kwargs)
        print("k: %s" % kwargs['initial'])
        return kwargs
    """

    def get_context_data(self, **kwargs):
        print("GET CONTEXT DATA")
        # Call the base implementation first to get a context
        context = super(CategoryDisplay, self).get_context_data(**kwargs)
        category = self.object
        print("Category: %s" % category)
        # Add in a QuerySet of all posts for the given estimates
        context['category'] = category
        self.fill_data(category, context)
        # context['product_list'] = categorie.products.filter(active=True)
        if self.request.user.role == ADMIN_ROLE:
            context['products_list'] = category.get_products()
        else:
            context['active_products_list'] = category.get_active_products()
        # context['form'].fields[key].widget.attrs['disabled'] = False
        # context['product_list'] = Product.objects.filter(category=categorie)
        return context

    def fill_data(self, category, context):
        print("Fill data in updateView")
        context['form'] = CategoryInterestForm(
            initial={
                'name': category.name,
                'description': category.description,
                'is_active': category.is_active,
            },
            is_hidden=self.request.user.role == USER_ROLE
        )


class AddCategoryView(UserCheckMixin, CreateView):

    model = Category
    template_name = "add_category.html"
    form_class = CategoryForm
    context_object_name = "category"
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"

    def get_success_url(self):
        return reverse('oscm:categories')


class DeleteCategoryView(UserCheckMixin, DeleteView):

    model = Category
    template_name = "delete_category.html"
    form_class = CategoryForm
    slug_field = "slug_name"
    slug_url_kwarg = "slug_name"

    def get_success_url(self):
        return reverse('oscm:categories')
