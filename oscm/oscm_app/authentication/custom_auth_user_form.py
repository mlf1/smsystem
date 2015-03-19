# oscm_app/authentication

from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext as _

from oscm_app.custom_auth_user import CustomAuthUser
from .custom_read_only_password_hash_widget import (
    CustomReadOnlyPasswordHashWidget)


class CustomAuthUserCreationForm(forms.ModelForm):
    """
    A form for creating new users. Includes all the required fields, plus a
    repeated password.
    """
    # Password
    password1 = forms.CharField(
        label=_('oscm_admin_passwordLabelOfUser'),
        widget=forms.PasswordInput)
    # Password confirmation
    # 'Enter the same password as above, for verification.''
    password2 = forms.CharField(
        label=_('oscm_admin_passwordConfirmationLabelOfUser'),
        widget=forms.PasswordInput,
        help_text=_('oscm_admin_helpTextPassword2fUser'))

    class Meta:
        model = CustomAuthUser
        fields = (
            'username',
            'email',
            'role',
            'language',
            'authentication_mode')

    def clean_username(self):
        """
        Check that the username is unique
        """
        username = self.cleaned_data["username"]
        try:
            CustomAuthUser._default_manager.get(username=username)
        except CustomAuthUser.DoesNotExist:
            return username
        # 'Username must be unique'
        raise forms.ValidationError(
            _('Duplicate username: %(value)s'),
            code='duplicate',
            params={'value': username},)

    def clean_password2(self):
        """
        Check that the two password entries match
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            # 'Passwords don't match'
            raise forms.ValidationError(
                _('Invalid passwords: %(password1)s, %(password2)s'),
                code='invalid',
                params={'password1': password1, 'password2': password2},)
        return password2

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        custom_user = super(CustomAuthUserCreationForm, self).save(
            commit=False)
        # Check the authentication mode
        auth_mode = custom_user.authentication_mode
        # TODO: Remove if it's working
        print("Auth_mode is {0}.", auth_mode)
        if auth_mode == 'D':
            custom_user.set_password(self.cleaned_data['password1'])
            if commit:
                custom_user.save()
            return custom_user
        else:
            if auth_mode == 'L':
                raise forms.ValidationError(
                    _('Invalid Ldap authentication: %(value)s'),
                    code='invalid',
                    params={'value': auth_mode},)
            else:
                raise forms.ValidationError(
                    _('Invalid authentication: %(value)s'),
                    code='invalid',
                    params={'value': auth_mode},)


class CustomAuthUserChangeForm(forms.ModelForm):
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

    class Meta:
        model = CustomAuthUser
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

    def clean_password(self):
        """
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the field
        doesn't have access to the initial value.
        """
        return self.initial['password']
