# oscm_app/register

from django.contrib.auth import (authenticate, login, get_user_model)
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.template import RequestContext
from django.utils.translation import ugettext as _
from django.views.generic.edit import CreateView

# from registration import signals

from .registration_forms import RegistrationFormTOS
from oscm_app.utils import get_attr


class Registration(CreateView):
    form_class = RegistrationFormTOS
    template_name = 'registration/registration.html'
    model = get_user_model()
    disallowed_url = 'registration_disallowed'
    success_url = 'registration/registration_completed.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Check that user signup is allowed before even bothering to
        dispatch or do other processing.
        """
        registration_allowed = self.registration_allowed(request)
        if not registration_allowed:
            return redirect(self.disallowed_url)
        return super(Registration, self).dispatch(
            request, *args, **kwargs)

    def form_valid(self, form):
        """
        Check if the form is valid.
        """
        validation = super(Registration, self).form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        print(_("OSCM User \'{0:s}\' is registered.").format(str(username)))
        if get_attr('REGISTRATION_AUTO_ACTIVATED_ACCOUNT', False):
            self.request.session.modified = True
            print(_("OSCM User \'{0:s}\' is logged in.").format(
                str(username)))
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
