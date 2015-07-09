# coding=utf-8
# oscm_app/authentication

from django import forms
from django.contrib.auth.hashers import (
    UNUSABLE_PASSWORD_PREFIX, identify_hasher)
from django.forms.utils import flatatt
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.utils.translation import ugettext as _


class CustomReadOnlyPasswordHashWidget(forms.Widget):

    """
    This widget is used to display the password field in the edit mode.
    """

    def render(self, name, value, attrs=None):
        """
        Redefine the render to have an error message if there is any error
        else an empty string ('').
        """
        encoded = value
        final_attrs = self.build_attrs(attrs)
        if not encoded or encoded.startswith(UNUSABLE_PASSWORD_PREFIX):
            summary = mark_safe("<strong>%s</strong>" % _(
                'oscm_admin_noPasswordSet'))
        else:
            try:
                identify_hasher(encoded)
            except ValueError:
                summary = mark_safe(
                    "<strong>%s</strong>" % _(
                        'oscm_admin_invalidPasswordFormatOrUnknownHashAlgo'))
            else:
                # Return empty string
                summary = ''

        return format_html("<div{0}>{1}</div>", flatatt(final_attrs), summary)
