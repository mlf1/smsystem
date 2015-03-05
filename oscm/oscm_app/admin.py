# oscm_app

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as OriginalUserAdmin
from django.utils.translation import ugettext as _

from .customAuthUser import CustomAuthUser
from oscm_app.authentication.customAuthUserForm import CustomAuthUserChangeForm, CustomAuthUserCreationForm


"""
Define a new User admin
"""
class UserAdmin(OriginalUserAdmin):
	# The forms to add and change user instances
	form = CustomAuthUserChangeForm
	add_form = CustomAuthUserCreationForm
	fieldsets = (
		(None, 
			{'fields': ('username', 'password')}),
		(_('oscm_admin_headerOfPersonalInfo'), 
			{'fields': ('first_name', 'last_name', 'email')}),
		(_('oscm_admin_headerOfCommonSettings'), 
			{'fields': ('authentication_mode',)}),
		(_('oscm_admin_headerOfPermissions'), 
			{'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
		(_('oscm_admin_headerOfUserSettings'), 
			{'fields': ('role', 'language')}),
		(_('oscm_admin_headerOfImportantDates'), 
			{'fields': ('last_login', 'date_joined')}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'email', 'password1', 'password2', 'role', 'language', 'authentication_mode')}
		),
	)
	list_display = ('username', 'email', 'role', 'language', 'authentication_mode', 'is_staff')
	list_display_links = ('username', 'email', 'role', 'language', 'authentication_mode', 'is_staff')
	list_filter = ('username', 'role', 'language')
	readonly_fields = ('last_login', 'date_joined')
	search_fields = ('username', 'email', 'role', 'language')
	ordering = ('username',)
	filter_horizontal = ('groups', 'user_permissions',)

admin.site.register(CustomAuthUser, UserAdmin) 