# oscm_app

from django.conf.urls import (patterns, url)

# Example 1: url(r'^welcome$', 'home'),
# Example 2: url(r'^$', "index", name='index'),


urlpatterns = patterns(
    'oscm_app.views',
    )

urlpatterns += patterns(
    'oscm_app.sign.log_views',
    url(r'^home$',
        'home_view',
        {'template_name': 'oscm_app/home.html'},
        prefix='',
        name='home'),
    url(r'^login$',
        'login_view',
        {'template_name': 'oscm_app/sign/login.html'},
        prefix='',
        name='login'),
    url(r'^logout$',
        'logout_view',
        {'template_name': 'oscm_app/sign/logout.html'},
        name='logout'),
    )
