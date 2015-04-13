# oscm_app

from django.conf.urls import (patterns, url)
from django.views.generic.base import TemplateView


urlpatterns = patterns(
    'oscm_app.views',
    url(r'^$', TemplateView.as_view(
        template_name='oscm_app/index.html'),
        name='index'),
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
