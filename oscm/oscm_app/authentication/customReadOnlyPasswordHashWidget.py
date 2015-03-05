# oscm_app/authentication

from django import forms
from django.contrib.auth.hashers import UNUSABLE_PASSWORD_PREFIX, identify_hasher
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.forms.utils import flatatt


class CustomReadOnlyPasswordHashWidget(forms.Widget):
	"""
	This widget is used to display the password filed in the edit mode.
	"""
	
	def render(self, name, value, attrs):
		"""
		Redefine the render to have an error message if there is any error else an empty string ('').
		"""
		encoded = value
		final_attrs = self.build_attrs(attrs)
		if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
			summary = mark_safe("<strong>%s</strong>" % ugettext("oscm_admin_noPasswordSet"))
		else:
			try:
				identify_hasher(encoded)
			except ValueError:
				summary = mark_safe("<strong>%s</strong>" % ugettext("oscm_admin_invalidPasswordFormatOrUnknownHashingAlgorithm"))
			else:
				# Return empty string
				summary = ''

		return format_html("<div{0}>{1}</div>", flatatt(final_attrs), summary)