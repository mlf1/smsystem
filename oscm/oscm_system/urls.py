# coding=utf-8
# oscm_system

# django imports
from django.conf.urls import (include, patterns, url)
from django.contrib import admin
from django.views.generic.base import RedirectView

urlpatterns = patterns(
    '',
    url(r'^$', RedirectView.as_view(
        permanent=False,
        pattern_name='oscm:index')),
    url(r'^oscm/', include('oscm_app.urls', namespace='oscm')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns(
    '',
    (r'^i18n/', include('django.conf.urls.i18n')),
)

handler403 = 'oscm_app.errors.error_views.permission_denied'
handler404 = 'oscm_app.errors.error_views.page_not_found'
handler500 = 'oscm_app.errors.error_views.server_error'

urlpatterns += patterns(
    '',
    url(r'^403$', handler403, name='403'),
    url(r'^404$', handler404, name='404'),
    url(r'^500$', handler500, name='500'),
)
