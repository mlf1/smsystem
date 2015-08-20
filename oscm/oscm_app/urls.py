# coding=utf-8
# oscm_app

# django imports
from django.conf.urls import (patterns, url)
from django.views.generic.base import TemplateView

# OSCM imports
from .cart.cart_views import (
    CartDisplay,
    CartInterest,
    CartsDisplay)
from .cart.catalogue.views.catalogue_views import (
    Catalogue,
)
from .cart.catalogue.views.category_views import (
    CategoriesDisplay,
    CategoryDisplay,
    CategoryInterest,
    AddCategoryView,
    DeleteCategoryView
)
from .cart.catalogue.views.product_views import (
    ProductsDisplay,
    ProductDisplay,
    ProductInterest,
    AddProductView,
    DeleteProductView
)
from .cart.catalogue.views.supplier_views import (
    SuppliersDisplay,
    SupplierDisplay,
    SupplierInterest,
    AddSupplierView,
    DeleteSupplierView
)
from .preferences.account_settings_view import AccountSettings
from .registration.registration_views import Registration

urlpatterns = patterns(
    'oscm_app.views',
    url(r'^$', TemplateView.as_view(
        template_name='oscm_app/index.html'),
        name='index'),
)

urlpatterns += patterns(
    'oscm_app.about.about_views',
    url(r'^about$', TemplateView.as_view(
        template_name='oscm_app/about/about.html'),
        name='about'),
)

urlpatterns += patterns(
    'oscm_app.sign.log_views',
    url(r'^home$',
        'home_view',
        {'template_name': 'oscm_app/home.html'},
        name='home'),
    url(r'^login$',
        'login_view',
        {'template_name': 'oscm_app/sign/login.html'},
        name='login'),
    url(r'^logout$',
        'logout_view',
        {'template_name': 'oscm_app/sign/logout.html',
         'next_page': '/oscm/'},
        name='logout'),
)

urlpatterns += patterns(
    'oscm_app.registration.registration_views',
    url(r'^register$', Registration.as_view(
        template_name='oscm_app/registration/registration.html',
        disallowed_url='oscm:registration_disallowed',
        success_url='oscm:registration_completed'),
        name='registration'),
    url(r'^register/closed/$', TemplateView.as_view(
        template_name='oscm_app/registration/registration_closed.html'),
        name='registration_disallowed'),
    url(r'^register/completed/$', TemplateView.as_view(
        template_name='oscm_app/registration/registration_completed.html'),
        name='registration_completed'),
)

urlpatterns += patterns(
    'oscm_app.preferences.account_settings_view',
    url(r'^home/settings/(?P<pk>\d+)/$', AccountSettings.as_view(
        template_name='oscm_app/preferences/settings.html',
        success_url='oscm:home'),
        name='account_settings'),
)

urlpatterns += patterns(
    'oscm_app.cart.catalogue_views',
    url(r'^home/catalogue$', Catalogue.as_view(
        template_name='oscm_app/cart/catalogue/catalogue.html'),
        name='catalogue'),
)

urlpatterns += patterns(
    'oscm_app.cart.catalogue.category_views',
    url(r'^home/catalogue/categories$', CategoriesDisplay.as_view(
        template_name='oscm_app/cart/catalogue/categories.html'),
        name='categories'),
    url(r'^home/catalogue/categories/(?P<slug_name>[-\w]+)/$',
        CategoryDisplay.as_view(
            template_name='oscm_app/cart/catalogue/category.html'),
        name='category'),
    url(r'^home/catalogue/categories/(?P<slug_name>[-\w]+)/details$',
        CategoryInterest.as_view(
            template_name='oscm_app/cart/catalogue/category_details.html',
            unsucess_template='oscm_app/cart/catalogue/category.html'),
        name='category_details'),
    url(r'^home/catalogue/categories/add$',
        AddCategoryView.as_view(
            template_name='oscm_app/cart/catalogue/add_category.html'),
        name='add_category'),
    url(r'^home/catalogue/categories/(?P<slug_name>[-\w]+)/del$',
        DeleteCategoryView.as_view(
            template_name='oscm_app/cart/catalogue/delete_category.html'),
        name='delete_category'),
)

urlpatterns += patterns(
    'oscm_app.cart.catalogue.product_views',
    url(r'^home/catalogue/products$',
        ProductsDisplay.as_view(
            template_name='oscm_app/cart/catalogue/products.html'),
        name='products'),
    url(r'^home/catalogue/products/(?P<slug_name>[-\w]+)/$',
        ProductDisplay.as_view(
            template_name='oscm_app/cart/catalogue/product.html'),
        name='product'),
    url(r'^home/catalogue/products/(?P<slug_name>[-\w]+)/details$',
        ProductInterest.as_view(
            template_name='oscm_app/cart/catalogue/product_details.html',
            unsucess_template='oscm_app/cart/catalogue/product.html'),
        name='product_details'),
    url(r'^home/catalogue/products/add$',
        AddProductView.as_view(
            template_name='oscm_app/cart/catalogue/add_product.html'),
        name='add_product'),
    url(r'^home/catalogue/products/(?P<slug_name>[-\w]+)/del$',
        DeleteProductView.as_view(
            template_name='oscm_app/cart/catalogue/delete_product.html'),
        name='delete_product'),
)

urlpatterns += patterns(
    'oscm_app.cart.catalogue.supplier_views',
    url(r'^home/catalogue/suppliers$', SuppliersDisplay.as_view(
        template_name='oscm_app/cart/catalogue/suppliers.html'),
        name='suppliers'),
    url(r'^home/catalogue/suppliers/(?P<slug_name>[-\w]+)/$',
        SupplierDisplay.as_view(
            template_name='oscm_app/cart/catalogue/supplier.html'),
        name='supplier'),
    url(r'^home/catalogue/suppliers/(?P<slug_name>[-\w]+)/details$',
        SupplierInterest.as_view(
            template_name='oscm_app/cart/catalogue/supplier_details.html',
            unsucess_template='oscm_app/cart/catalogue/supplier.html'),
        name='supplier_details'),
    url(r'^home/catalogue/supplier/add$',
        AddSupplierView.as_view(
            template_name='oscm_app/cart/catalogue/add_supplier.html'),
        name='add_supplier'),
    url(r'^home/catalogue/suppliers/(?P<slug_name>[-\w]+)/del$',
        DeleteSupplierView.as_view(
            template_name='oscm_app/cart/catalogue/delete_supplier.html'),
        name='delete_supplier'),
)

urlpatterns += patterns(
    'oscm_app.cart.cart_views',
    url(r'^home/carts/(?P<pk>\d+)$', CartsDisplay.as_view(
        template_name='oscm_app/cart/carts.html'),
        name='carts'),
    url(r'^home/carts/cart/(?P<pk>\d+)/$', CartDisplay.as_view(
        template_name='oscm_app/cart/cart.html'),
        name='cart'),
    url(r'^home/carts/cart/(?P<pk>\d+)/details$', CartInterest.as_view(
        template_name='oscm_app/cart/cart_details.html',
        unsucess_template='oscm_app/cart/cart.html'),
        name='cart_details'),
)
