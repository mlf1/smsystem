# coding=utf-8
# oscm_app/cart

# django imports
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _


class CartAdmin(admin.ModelAdmin):
    fieldsets = [
        (_('oscm_admin_informationHeaderOfCart'),  {'fields': [
            'project_name',
            'owner',
            'description',
            'requested_due_date']}),
        (_('oscm_admin_headerOfStatus'), {'fields': ['status']}),
        (_('oscm_admin_headerOfImportantDates'), {'fields': [
            'creation_date',
            'last_edit_date']}),
    ]
    list_display = (
        'project_name',
        'owner',
        'description',
        'requested_due_date',
        'status',
    )
    list_display_links = (
        'project_name',
        'owner',
        'description',
        'requested_due_date',
        'status',
    )
    list_filter = ('project_name', 'status', 'owner')
    readonly_fields = ('last_edit_date', 'creation_date')
    ordering = ('requested_due_date', 'status', 'owner', 'project_name')
    search_fields = ['requested_due_date', 'status', 'owner', ]
