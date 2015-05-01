# oscm_app/register

import logging

from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from oscm_app.authentication.custom_auth_user_form import (
    CustomAuthUserCreationForm)
from oscm_app.utils import get_attr

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RegistrationFormTOS(CustomAuthUserCreationForm):

    """
    Subclass of ``CustomAuthUserCreationForm`` which adds a required checkbox
    for agreeing to a site's Terms of Service.
    """

    tos = forms.BooleanField(
        widget=forms.CheckboxInput,
        label=_('I have read and agree to the Terms of Service'),
        error_messages={'required': _(
            "You must agree to the terms to register")})

    excluded_fields = None

    class Meta:
        model = get_user_model()
        fields = (
            'username',
            'email',
            'role',
            'language',
            'authentication_mode')
        exclude = ('role', 'authentication_mode',)

    def __init__(self, *args, **kwargs):
        super(RegistrationFormTOS, self).__init__(*args, **kwargs)
        self.set_excluded_fields()
        self.remove_excluded_fields()

    def set_excluded_fields(self):
        """
        Retrieve the excluded fields.
        """
        # Retrieve the excluded fields from the model (normal way)
        self.excluded_fields = list(getattr(self.Meta, 'exclude', []))
        # Retrieve the fields which have just one choice
        self.set_fields_with_one_choice(self.excluded_fields)

    def set_fields_with_one_choice(self, excluded_fields_list):
        """
        Retrieve the fields which have just one choice.
        """
        for field_name in self.fields:
            if (hasattr(self.fields[field_name], 'choices')
                    and len(self.fields[field_name].choices) == 1):
                logger.debug(_(
                    "Appends the \'{0:s}\' field to the excluded fields "
                    "list.".format(field_name)))
                excluded_fields_list.append(field_name)

    def remove_excluded_fields(self):
        """
        Remove excluded fields from the form.
        """
        if self.excluded_fields:
            for field_name in self.excluded_fields:
                if field_name in self.fields:
                    logger.debug(_("Remove %s field." % field_name))
                    del self.fields[field_name]

    def save_account(self, custom_user, commit=True):
        """
        Check configuration parameters and save account of the OSCM User.
        """
        custom_user = super(RegistrationFormTOS, self).save_account(
            custom_user,
            commit=False)
        if get_attr('REGISTRATION_AUTO_ACTIVATED_ACCOUNT', False):
            # Activated OSCM account
            custom_user.is_active = True
            logger.info(
                _("OSCM User \'%s\' is activated." % custom_user.username))
        else:
            logger.info(
                _("OSCM User \'%s\' is not yet activated." % (
                    custom_user.username)))
        if commit:
            custom_user.save()
            logger.info(
                _("OSCM User \'%s\' is registered." % custom_user.username))
        return custom_user
