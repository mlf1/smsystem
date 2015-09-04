# coding=utf-8
# oscm_app

# django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.utils.translation import ugettext as _

# OSCM imports
from .cart.admin import CartAdmin
from .cart.admin import CartItemAdmin
from .cart.catalogue.admin import (CategoryAdmin, ProductAdmin, SupplierAdmin)
from .cart.catalogue.models.category import Category
from .cart.catalogue.models.product import Product
from .cart.catalogue.models.supplier import Supplier
from .cart.models.cart import Cart
from .cart.models.cart_item import CartItem
from .custom_auth_user import CustomAuthUser
from .authentication.custom_auth_user_form import (
    CustomAuthUserChangeForm,
    CustomAuthUserCreationForm)


def export_csv(modeladmin, request, queryset):
    import csv
    from django.http import HttpResponse
    from django.utils.encoding import smart_str
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s.csv' % (
        str(opts).replace('.', '_')
    )
    writer = csv.writer(response, csv.excel)
    # BOM (optional...Excel needs it to open UTF-8 file properly)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Title"),
        smart_str(u"Description"),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.name),
            smart_str(obj.description),
        ])
    return response
export_csv.short_description = u"Export CSV"


class UserAdmin(OriginalUserAdmin):

    """
    Define a new User admin
    """
    # The forms to add and change user instances
    form = CustomAuthUserChangeForm
    add_form = CustomAuthUserCreationForm
    fieldsets = (
        (None, {'fields': (
            'username',
            'password')}),
        (_('oscm_admin_headerOfPersonalInfo'), {'fields': (
            'first_name',
            'last_name',
            'email')}),
        (_('oscm_admin_headerOfCommonSettings'), {'fields': (
            'authentication_mode',)}),
        (_('oscm_admin_headerOfPermissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions')}),
        (_('oscm_admin_headerOfUserSettings'), {'fields': (
            'role',
            'language')}),
        (_('oscm_admin_headerOfImportantDates'), {'fields': (
            'last_login',
            'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username',
                'email',
                'password1',
                'password2',
                'role',
                'language',
                'authentication_mode')}),
    )
    list_display = (
        'username',
        'email',
        'role',
        'language',
        'authentication_mode',
        'is_active',
        'is_staff')
    list_display_links = (
        'username',
        'email',
        'role',
        'language',
        'authentication_mode',
        'is_active',
        'is_staff')
    list_filter = ('username', 'role', 'language', 'is_active')
    readonly_fields = ('last_login', 'date_joined')
    search_fields = ('username', 'email', 'role', 'language')
    ordering = ('username',)
    filter_horizontal = ('groups', 'user_permissions',)

# admin.site.add_action(export_csv, 'CSV')

admin.site.register(CustomAuthUser, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartItem, CartItemAdmin)
