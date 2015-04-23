# oscm_system

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

handler404 = 'oscm_app.errors.error_views.page_not_found'
handler500 = 'oscm_app.errors.error_views.server_error'
