# oscm_app/authentication

import logging

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy as _

from .custom_read_only_password_hash_widget import (
    CustomReadOnlyPasswordHashWidget)
from oscm_app.utils import get_attr

# Get an instance of a logger
logger = logging.getLogger(__name__)


class BaseCustomAuthUserForm(forms.ModelForm):

    """
    Base form of the CustomAuthUser.
    """

    error_messages = {
        'duplicate username': _('Duplicate username: %(username)s'),
        'duplicate email': _('Duplicate email: %(email)s'),
        'invalid passwords': _(
            'Invalid passwords: %(password1)s, %(password2)s'),
        'invalid authentication': _(
            'Invalid authentication: %(authentication)s'),
        'invalid Ldap authentication': _(
            'Invalid Ldap authentication: %(authentication)s')
    }

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = get_user_model()
        fields = (
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'role',
            'language',
            'authentication_mode',
            'is_active',
            'is_staff',
            'is_superuser',
            'user_permissions')

    def clean_role(self):
        """
        If Role=Manager, the OSCM's user account will set 'is_staff' to
        'True'.
        If Role=Admin, the OSCM's user account will set 'is_staff' to 'True'
        and 'is_superuser' to 'True' too.
        """
        role = self.cleaned_data['role']
        logger.debug(_("Role is \'%s\'." % role))
        if role == 'A':
            self.cleaned_data['is_staff'] = True
            self.cleaned_data['is_superuser'] = True
        elif role == 'M':
            self.cleaned_data['is_staff'] = True
            self.cleaned_data['is_superuser'] = False
        else:
            logger.debug(_("There is no rights for the \'%s\' role." % dict(
                get_attr('USER_ROLES')).get(role)))
            self.cleaned_data['is_staff'] = False
            self.cleaned_data['is_superuser'] = False
        return role


class CustomAuthUserCreationForm(BaseCustomAuthUserForm):

    """
    A form for creating new users. Includes all the required fields, plus a
    repeated password.
    """
    # Password
    password1 = forms.CharField(
        label=_('oscm_admin_passwordLabelOfUser'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _(
                'oscm_admin_passwordLabelOfUser')}))
    # Password confirmation
    # 'Enter the same password as above, for verification.''
    password2 = forms.CharField(
        label=_('oscm_admin_passwordConfirmationLabelOfUser'),
        widget=forms.PasswordInput(attrs={
            'placeholder': _(
                'oscm_admin_passwordConfirmationLabelOfUser')}),
        help_text=_('oscm_admin_helpTextPassword2fUser'))

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = get_user_model()
        fields = (
            'username',
            'email',
            'role',
            'language',
            'authentication_mode')

    def __init__(self, *args, **kwargs):
        super(CustomAuthUserCreationForm, self).__init__(*args, **kwargs)
        # Added 'placeholder' field
        for name, field in self.fields.items():
            if name == 'username':
                field.widget.attrs.update({
                    'placeholder': _('oscm_admin_usernameOfUser')})
                continue
            if name == 'email':
                field.widget.attrs.update({
                    'placeholder': _('oscm_admin_emailAddressOfUser')})
                continue

    def clean_username(self):
        """
        Check that the username is unique
        """
        username = self.cleaned_data["username"]
        try:
            get_user_model()._meta.model._default_manager.get(
                username__iexact=username)
        except get_user_model()._meta.model.DoesNotExist:
            return username
        # 'Username must be unique'
        logger.error(
            self.error_messages['duplicate username'] % {
                'username': username})
        raise forms.ValidationError(
            self.error_messages['duplicate username'],
            code='duplicate',
            params={'username': username},)

    def clean_email(self):
        """
        Check that the email is unique
        """
        email = self.cleaned_data["email"]
        try:
            get_user_model()._meta.model._default_manager.get(
                email__iexact=email)
        except get_user_model()._meta.model.DoesNotExist:
            return email
        # 'email must be unique'
        logger.error(self.error_messages['duplicate email'] % {
            'email': email})
        raise forms.ValidationError(
            self.error_messages['duplicate email'],
            code='duplicate',
            params={'email': email},)

    def clean_password2(self):
        """
        Check that the two password entries match
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            # 'Passwords don't match'
            logger.error(self.error_messages['invalid passwords'] % {
                'password1': password1,
                'password2': password2})
            raise forms.ValidationError(
                self.error_messages['invalid passwords'],
                code='invalid',
                params={'password1': password1, 'password2': password2},)
        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        custom_user = super(CustomAuthUserCreationForm, self).save(
            commit=False)
        return self.save_account(custom_user, commit)

    def save_account(self, custom_user, commit=True):
        """
        Save the account of the OSCM User.
        """
        # Check the authentication mode
        auth_mode = custom_user.authentication_mode
        # TODO: Remove if it's working
        logger.debug(_("Auth_mode is \'%s\'." % auth_mode))
        if auth_mode == 'D':
            custom_user.set_password(self.cleaned_data['password1'])
        else:
            if auth_mode == 'L':
                logger.error(self.error_messages[
                    'invalid Ldap authentication'] % {'value': auth_mode})
                raise forms.ValidationError(
                    self.error_messages['invalid Ldap authentication'],
                    code='invalid',
                    params={'value': auth_mode},)
            else:
                logger.error(self.error_messages[
                    'invalid authentication'] % {'authentication': auth_mode})
                raise forms.ValidationError(
                    self.error_messages['invalid authentication'],
                    code='invalid',
                    params={'value': auth_mode},)
        if self.has_changed() or commit:
            custom_user.save()
            logger.info(
                _(
                    "OSCM User \'%s\' is "
                    "registered." % custom_user.username))
        return custom_user


class CustomAuthUserChangeForm(BaseCustomAuthUserForm):

    """
    A form for updating users. Includes all the fields on the user.

    Raw passwords are not stored, so there is no way to see this user's
    password, but you can change the password using <a href=\"password/\">
    this form</a>.
    """
    password = ReadOnlyPasswordHashField(
        label=_('oscm_admin_passwordLabelOfUser'),
        help_text=_('oscm_admin_helpTextPasswordOfUser'),
        widget=CustomReadOnlyPasswordHashWidget)

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the field
        doesn't have access to the initial value.
        """
        return self.initial['password']
