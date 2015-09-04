# coding=utf-8
# oscm_app/preferences

# python imports
import logging

# django imports
from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _

# OSCM imports
from ..authentication.custom_auth_user_form import (
    BaseCustomAuthUserForm)
from ..utils import set_form_field_order


# Get an instance of a logger
logger = logging.getLogger(__name__)


class AccountSettingsForm(BaseCustomAuthUserForm):

    """
    This class is the specific form of the OSCM User settings.
    """
    has_been_modified = True

    class Meta:

        """
        Use this Meta class on any model to specify various
        model-specific options.
        """
        model = get_user_model()
        fields = (
            'username',
            'email',
            'language',)

    def __init__(self, *args, **kwargs):
        initial = kwargs.pop("initial", {})
        kwargs['initial'] = self.retrieve_initial_data(
            initial,
            *args,
            **kwargs)
        super(AccountSettingsForm, self).__init__(*args, **kwargs)
        set_form_field_order(self, ["username", "email", "language"])

    def retrieve_initial_data(self, initial, *args, **kwargs):
        """
        Populate initial with its field values.
        """
        if kwargs.get("instance"):
            current_user = kwargs["instance"]
            for key in self.Meta.fields:
                if hasattr(current_user, key):
                    initial[key] = initial.get(key) or getattr(
                        current_user,
                        key)
        return initial

    def clean_username(self):
        username = self.cleaned_data['username']
        if username != self.initial['username']:
            logger.debug("Different username")
            users = get_user_model().objects.filter(
                username__iexact=username)
            if users:
                logger.error(self.error_messages['duplicate username'] % {
                    'username': username})
                raise forms.ValidationError(
                    self.error_messages['duplicate username'],
                    code='duplicate',
                    params={'username': username},)
            return username
        else:
            return self.initial['username']

    def clean_email(self):
        email = self.cleaned_data['email']
        if email != self.initial['email']:
            logger.debug("Different email")
            users = get_user_model().objects.filter(
                email__iexact=email)
            if users:
                logger.error(self.error_messages['duplicate email'] % {
                    'email': email})
                raise forms.ValidationError(
                    self.error_messages['duplicate email'],
                    code='duplicate',
                    params={'email': email},)
            return email
        else:
            return self.initial['email']

    def clean_language(self):
        language = self.cleaned_data['language']
        if self.initial['language'] == language:
            logger.debug("No modificaton with the language !! %s" % language)
            return self.initial['language']
        else:
            logger.debug("Return language from the settings: %s" % language)
            return language

    def clean(self):
        """
        Use a specific clean method for the current form.
        """
        # Ensures that any validation logic in parent classes is maintained.
        super(AccountSettingsForm, self).clean()
        if self._errors:
            return
        if (self.cleaned_data['username'] == self.initial['username']
                and self.cleaned_data['email'] == self.initial['email']
                and self.cleaned_data['language'] == self.initial['language']):
            self.has_been_modified = False
            logger.debug(_("No field has been modified."))
            return
        return self.cleaned_data

    def save(self, commit=True):
        """
        Save the provided password in hashed format
        """
        custom_user = super(BaseCustomAuthUserForm, self).save(
            commit=False)
        return self.save_account(custom_user, commit)

    def save_account(self, custom_user, commit=True):
        """
        Save the account of the OSCM User if it is necessary.
        """
        if commit and self.has_been_modified:
            custom_user.save()
            # Set the initial state
            self.has_been_modified = False
            logger.info(
                _(
                    "OSCM Account settings from the OSCM User \'%s\' has "
                    "been updated." % custom_user.username))
            return custom_user
