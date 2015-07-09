# coding=utf-8
# oscm_app/preferences

import logging

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.core.urlresolvers import reverse
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

from .account_settings_form import AccountSettingsForm
from oscm_app.decorators.user_check_mixin import UserCheckMixin

# Get an instance of a logger
logger = logging.getLogger(__name__)


class AccountSettings(UserCheckMixin, UpdateView):

    """
    This class is used to keep the specific parameters
    for the OSCM User in the frontend.
    """

    template_name = "account/settings.html"
    form_class = AccountSettingsForm
    redirect_field_name = "next"
    success_url = None
    model = get_user_model()
    messages = {
        "settings_updated": {
            "level": messages.SUCCESS,
            "text": _("OSCM Account settings updated.")
        },
    }

    def get_context_data(self, **kwargs):
        context = super(AccountSettings, self).get_context_data(**kwargs)
        return context

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        self.object = form.save()
        # Set the user's language if necessary
        current_language = translation.get_language()
        user_language = self.get_object().language
        if current_language != user_language:
            logger.debug(
                "Change the current language \'%s\' to \'%s\'." % (
                    current_language, user_language))
            # "activate()"" works only for the current view
            translation.activate(user_language)
            # Set the session variable
            self.request.session[
                translation.LANGUAGE_SESSION_KEY] = user_language
            # self.request.session['django_language'] = user_language
            # self.request.LANGUAGE_CODE = translation.get_language()
        if self.object:
            messages.add_message(
                self.request,
                self.messages['settings_updated']['level'],
                self.messages['settings_updated']['text'])
        return super(AccountSettings, self).form_valid(form)

    def get_success_url(self):
        return reverse(self.success_url)
