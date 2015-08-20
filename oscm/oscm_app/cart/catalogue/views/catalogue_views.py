# coding=utf-8
# oscm_app/cart/catalogue

# django imports
from django.views.generic import TemplateView

# OSCM imports
from ....decorators.user_check_mixin import UserCheckMixin


class Catalogue(UserCheckMixin, TemplateView):

    """
    This class represents the catalogue with its categories and its products.
    """

    def get(self, request, *args, **kwargs):
        """
        Gets a specific product.
        """
        # Code
        return super(Catalogue, self).get(request, *args, **kwargs)

    def get_search_handler(self, *args, **kwargs):
        """
        Searchs a specific product.
        """
        # Code
        return

    def get_context_data(self, **kwargs):
        """
        Gets context data.
        """
        """
        ctx = {}
        ctx['summary'] = _('oscm_allProductsOfCatalogue')
        search_context = null
        ctx.update(search_context)
        return ctx
        """
        context = super(Catalogue, self).get_context_data(**kwargs)
        print("CONTEXT CATALOGUE: %s" % context)
        return context
