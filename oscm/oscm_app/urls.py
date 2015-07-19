# coding=utf-8
# oscm_app

# django imports
from django.conf.urls import (patterns, url)
from django.views.generic.base import TemplateView

# OSCM imports
from .preferences.account_settings_view import AccountSettings
from .registration.registration_views import Registration

urlpatterns = patterns(
    'oscm_app.views',
    url(r'^$', TemplateView.as_view(
        template_name='oscm_app/index.html'),
        name='index'),
)

urlpatterns += patterns(
    'oscm_app.about.about_views',
    url(r'^about$', TemplateView.as_view(
        template_name='oscm_app/about/about.html'),
        name='about'),
)

urlpatterns += patterns(
    'oscm_app.sign.log_views',
    url(r'^home$',
        'home_view',
        {'template_name': 'oscm_app/home.html'},
        name='home'),
    url(r'^login$',
        'login_view',
        {'template_name': 'oscm_app/sign/login.html'},
        name='login'),
    url(r'^logout$',
        'logout_view',
        {
            'template_name': 'oscm_app/sign/logout.html',
            'next_page': '/oscm/'},
        name='logout'),
)

urlpatterns += patterns(
    'oscm_app.registration.registration_views',
    url(r'^register$', Registration.as_view(
        template_name='oscm_app/registration/registration.html',
        disallowed_url='oscm:registration_disallowed',
        success_url='oscm:registration_completed'),
        name='registration'),
    url(r'^register/closed/$', TemplateView.as_view(
        template_name='oscm_app/registration/registration_closed.html'),
        name='registration_disallowed'),
    url(r'^register/completed/$', TemplateView.as_view(
        template_name='oscm_app/registration/registration_completed.html'),
        name='registration_completed'),
)

urlpatterns += patterns(
    'oscm_app.preferences.oscm_account_settings_view',
    url(r'^home/settings/(?P<pk>\d+)/$', AccountSettings.as_view(
        template_name='oscm_app/preferences/settings.html',
        success_url='oscm:home'),
        name='account_settings'),
)
