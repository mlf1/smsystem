# coding=utf-8
# oscm_app/cart/catalogue

# django imports
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class CategoryAdmin(admin.ModelAdmin):
    # actions=[export_csv]
    view_on_site = False
    prepopulated_fields = {"slug_name": ('name', )}


class SupplierAdmin(admin.ModelAdmin):
    view_on_site = False
    prepopulated_fields = {"slug_name": ('name', )}


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug_name": ('name', )}
    fieldsets = [
        ('Product information',  {'fields': [
            'name',
            'slug_name',
            'description',
            'unit_price',
            'quantity',
            'sku',
            'is_active']}),
        (_('oscm_admin_headerOfCategory'), {'fields': ['category']}),
        # (_('oscm_admin_headerOfSupplier'), {'fields': ['supplier']}),
        (_('oscm_admin_headerOfImportantDates'), {'fields': [
            'creation_date',
            'last_edit_date']}),
    ]
    list_display = (
        'name',
        'description',
        'code',
        'unit_price',
        'quantity',
        'sku',
        'is_active',
    )
    list_display_links = (
        'name',
        'description',
        'code',
        'unit_price',
        'quantity',
        'sku',
        'is_active',
    )
    list_filter = ('is_active', 'category')
    readonly_fields = ('last_edit_date', 'creation_date')
    # ordering = ('creation_date', 'name', 'category', 'supplier')
    ordering = ('creation_date', 'name', 'category')
    search_fields = ['name', 'code', 'category', ]
