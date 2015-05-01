# oscm_app/sign

# from django.contrib import messages
import logging

from django.contrib.auth import (login, logout)
from django.contrib.auth.decorators import login_required
from django.core.context_processors import csrf
from django.core.urlresolvers import (get_script_prefix, reverse)
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from .log_forms import LoginForm
from oscm_app.utils import (get_attr, next_url)

# Get an instance of a logger
logger = logging.getLogger(__name__)


@login_required
def home_view(request, template_name='home.html'):
    """
    This is the home page of the OSCM User.
    """
    loggedin = request.user.is_authenticated()
    return render(
        request,
        template_name,
        {'loggedin': loggedin, 'request': request})


@login_required
def logout_get_view(request):
    """
    Logout the current OSCM User.
    """
    logout(request)
    return HttpResponseRedirect(reverse('oscm:index'))


@login_required
def logout_view(request, template_name='logout.html', next_page=None):
    """
    Display the logout and handles the logout action.
    """
    if request.method == 'POST':
        username = request.user.username
        # Since we know the user is logged in, we can now just log them out.
        logout(request)
        logger.info(_("OSCM User \'{0:s}\' is logged out.").format(
            str(username)))
        # Set the user's language if necessary
        current_language = translation.get_language()
        default_language = get_attr('LANGUAGE_CODE')
        if current_language != default_language:
            logger.debug(
                _(
                    "Change the current language \'%(current_language)s\' "
                    "to \'%(default_language)s\'."), {
                        "current_language": current_language,
                        "default_language": default_language})
            # "activate()"" works only for the current view
            translation.activate(default_language)
            # Set the session variable
            request.session[
                translation.LANGUAGE_SESSION_KEY] = default_language
        # messages.success(request, _("You have been logged out."))
        return HttpResponseRedirect(next_url(request) or get_script_prefix())
    else:
        context = {"title": _("Log out"), "next": next_page}
        context.update(csrf(request))
        return render(request, template_name, context)


@sensitive_post_parameters()
def login_view(request, template_name='login.html'):
    """
    Display the login form and handles the login action.
    """
    # If the request is a HTTP POST, try to pull out the relevant information.
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.login(request)
        if user is None:
            # Return an 'invalid login' error message
            logger.info(_("OSCM User with \'{0:s}\' is invalid!!").format(
                request.username))
            return HttpResponseRedirect(reverse('oscm:home'))
        else:
            if user.is_active:
                login(request, user)
                logger.info(_("OSCM User \'{0:s}\' is logged in.").format(
                    str(user.username)))
                # Set the user's language if necessary
                current_language = translation.get_language()
                user_language = user.language
                if current_language != user_language:
                    logger.debug(
                        _(
                            "Change the current language "
                            "\'%(current_language)s\' to "
                            "the OSCM User's language "
                            "\'%(user_language)s\'."), {
                                "current_language": current_language,
                                "user_language": user_language})
                    # "activate()"" works only for the current view
                    translation.activate(user_language)
                    # Set the session variable
                    request.session[
                        translation.LANGUAGE_SESSION_KEY] = user_language
                return HttpResponseRedirect(reverse('oscm:home'))
            else:
                # Return a 'disabled account' error message
                logger.info(_("OSCM User \'{0:s}\' is inactive!!").format(
                    str(user.username)))
                return HttpResponseRedirect(reverse('oscm:home'))
    else:
        context = {"form": form, "title": _("Log in")}
        context.update(csrf(request))
        # TODO: we must use reverse to avoid the hardcoded url path.
        # <code>return render(request, reverse(\'oscm:home\'), context)</code>
        return render(request, template_name, context)
