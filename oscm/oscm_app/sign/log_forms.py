# oscm_app/sign

# python imports
import logging

# django imports
from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

# OSCM imports
from ..utils import (get_attr, set_form_field_order)

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LoginForm(forms.Form):

    """
    This form is used to log the OSCM User in the frontend.
    """

    username = forms.CharField(
        max_length=255,
        required=True,
        label=_('Username'),
        widget=forms.TextInput(attrs={
            'placeholder': _('Username'),
            'autofocus': 'autofocus'}))
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            render_value=False,
            attrs={'placeholder': _('Password')}),
        required=True)
    remember = forms.BooleanField(
        label=_("Remember Me"),
        required=False,
        help_text=_("If checked you will stay logged in for 3 weeks."))
    user = None

    error_messages = {
        'account_inactive':
            _("This account is currently inactive."),
        'username_password_mismatch':
            _("The username and/or password you specified are not correct."),
    }

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, ["username", "password", "remember"])
        if get_attr('SESSION_REMEMBER') is not None:
            del self.fields['remember']

    def clean_username(self):
        """
        Clean the username.
        """
        username = self.cleaned_data['username']
        return username.strip()

    def clean(self):
        """
        Clean the "LoginForm".
        """
        # Ensures that any validation logic in parent classes is maintained.
        super(LoginForm, self).clean()
        if self._errors:
            return
        self.auth_user()
        return self.cleaned_data

    def login(self, request):
        logger.debug(_("OSCM User: \'%s\'." % self.user))
        if self.user is None:
            self.user = self.auth_user()
        remember = get_attr('SESSION_REMEMBER')
        if remember is None:
            remember = self.cleaned_data['remember']
        if remember:
            request.session.set_expiry(get_attr('SESSION_COOKIE_AGE'))
        else:
            request.session.set_expiry(0)
        return self.user

    def auth_user(self):
        """
        Authenticate the user with the username and the password
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                # An inactive account was used - no logging in!
                logger.error(_(
                    "No logging in! An inactive account was used with the "
                    "following OSCM User: \'{0}\'.").format(username))
                raise forms.ValidationError(
                    self.error_messages['account_inactive'])
            else:
                self.user = user
        else:
            # Bad login details were provided. So we can't log the user in.
            logger.error(_(
                "Invalid login details: "
                "username=\'{0}\', password=\'{1}\'.").format(
                    username,
                    password))
            raise forms.ValidationError(
                self.error_messages['username_password_mismatch'])
