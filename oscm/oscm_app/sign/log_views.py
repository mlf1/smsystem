# oscm_app/sign

# from django.contrib import messages
from django.contrib.auth import (authenticate, login, logout)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.context_processors import csrf
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.loader import get_template
from django.utils.translation import ugettext as _
from django.views.decorators.debug import sensitive_post_parameters

from .log_forms import LoginForm


"""
class LoginFormView view:
    form_class =
    initial =
    template_name =
"""


# @login_required
def home_view(request, template_name='home.html'):
    """
    This is the home page of the user.
    """
    t = get_template(template_name)
    print(t)
    loggedin = request.user.is_authenticated()
    # return HttpResponseRedirect(reverse('oscm:home'))
    return render(
        request,
        template_name,
        {'loggedin': loggedin, 'request': request})


@login_required
def logout_view(request, template_name):
    """
    Display the logout and handles the logout action.
    """
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(template_name)


@sensitive_post_parameters()
def login_view(request, template_name):
    """
    Display the login form and handles the login action.
    """

    print("T_N: ", template_name)
    # If the request is a HTTP POST, try to pull out the relevant information.
    form = LoginForm(request.POST or None)
    print("Retrieve LoginForm.")

    if form.is_valid():
        print("LoginForm is valid.")
        user = form.login(request)
        if user is None:
            # Return an 'invalid login' error message
            return HttpResponseRedirect('/logger/invalid_login/')
    else:
        print("LoginForm is invalid!!")
        # Return an 'invalid form' error message
        context = {"form": form, "title": _("Log in")}
        print(context)
        context.update(csrf(request))
        """
        TODO: we must use reverse to avoid the hardcoded url path
        return render(request, reverse('oscm:home'), context)
        """
        return render(request, 'oscm_app/home.html', context)

"""
@sensitive_post_parameters()
def login_view(request):

    Display the login form and handles the login action.

    # If the request is a HTTP POST, try to pull out the relevant information.
    form = LoginForm(request.POST or None)
    print(form.is_valid())
    if form.is_valid():
        print("LoginForm is valid.")
        is_remember = form.cleaned_data['remember']
        user = form.login(request)
        if user is None:
            # Return an 'invalid login' error message
            return HttpResponseRedirect('/logger/invalid_login/')
        else:
            if user.is_active:
                request = check_is_remember(request, is_remember)
                login(request, user)
                messages.success(
                    request,
                    _('You have successfully logged in'))
                print('User {"%s"} is logged.' % user)
                return HttpResponseRedirect(reverse('oscm:home'))
            else:
                # Return a 'disabled account' error message
                messages.error(
                    request,
                    _(
                        'Ihr Account wurde deaktiviert. Bitte nehmen Sie '
                        'Kontakt zu uns auf, wenn Sie Ihnen wieder '
                        'aktivieren wollen.'))
                return HttpResponseRedirect('/logger/bad_login/')
    else:
        # Return an 'invalid form' error message
        context = {"form": form, "title": _("Log in")}
        print(context)
        context.update(csrf(request))
        # return render(request, 'oscm_app/sign/login.html', context)
        return render(request, reverse('oscm:login'), context)
"""


def check_is_remember(request, is_remember):
    """
    Check if the session must be keep more one connection
    """
    if is_remember:
        # Set session timeout.
        # Multiply the days with 60 * 60 * 24,
        # because it was in day.
        print("is_remember: ", is_remember)
        request.session.set_expiry(60 * 60 * 24 * 3)
    else:
        # Set session timeout. Multiply the minutes with 60,
        # because it was in sec.
        print("is_remember: ", is_remember)
        request.session.set_expiry(60 * 30)
        # info(request, _("You have successfully logged in"))
        # reverse('index')
    return request
