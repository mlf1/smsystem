# coding=utf-8
# oscm_app/register

# python imports
import logging

# django imports
from django.contrib import messages
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.utils import translation
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import CreateView

# from registration import signals

# OSCM imports
from .registration_forms import RegistrationFormTOS
from ..utils import get_attr

# Get an instance of a logger
logger = logging.getLogger(__name__)


class Registration(CreateView):

    """
    This class is used for the registration view.
    """

    form_class = RegistrationFormTOS
    template_name = 'registration/registration.html'
    model = get_user_model()
    disallowed_url = 'registration_disallowed'
    success_url = 'registration/registration_completed.html'
    messages = {
        "account_created": {
            "level": messages.SUCCESS,
            "text": _("OSCM Account created.")
        },
        "account_activated": {
            "level": messages.SUCCESS,
            "text": _("Your OSCM Account has been activated.")
        },
        "account_not_activated": {
            "level": messages.WARNING,
            "text": _("But your OSCM Account is not yet activated.")
        },
    }

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        """
        registration_allowed = self.registration_allowed(request)
        if not registration_allowed:
            logger.debug(_("Registration is closed."))
            return redirect(self.disallowed_url)
        return super(Registration, self).dispatch(
            request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
        Inject 'title' into the context.
        """
        context = super(Registration, self).get_context_data(**kwargs)
        context['title'] = _('Register')
        return context

    def form_valid(self, form):
        """
        Check if the form is valid.
        """
        validation = super(Registration, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        if get_attr('REGISTRATION_AUTO_ACTIVATED_ACCOUNT', False):
            self.request.session.modified = True
            logger.info(_("OSCM User \'{0:s}\' is logged in.").format(
                str(username)))
            # Set the user's language if necessary
            current_language = translation.get_language()
            user_language = user.language
            if current_language != user_language:
                logger.debug(
                    "Change the current language \'%s\' to \'%s\'." % (
                        current_language, user_language))
                # "activate()"" works only for the current view
                translation.activate(user_language)
                # Set the session variable
                self.request.session[
                    translation.LANGUAGE_SESSION_KEY] = user_language
        else:
            logout(self.request)
        if self.object:
            messages.add_message(
                self.request,
                self.messages['account_created']['level'],
                self.messages['account_created']['text'])
            print("is_active: %s" % user.is_active)
            if user.is_active:
                messages.add_message(
                    self.request,
                    self.messages['account_activated']['level'],
                    self.messages['account_activated']['text'])
            else:
                messages.add_message(
                    self.request,
                    self.messages['account_not_activated']['level'],
                    self.messages['account_not_activated']['text'])
        return validation

    def get_success_url(self):
        return reverse(self.success_url)

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return get_attr('REGISTRATION_OPEN', True)
