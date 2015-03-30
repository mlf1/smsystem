from django.conf.urls import (patterns, include, url, handler404, handler500)
from django.contrib import admin


urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'oscm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^oscm/', include('oscm_app.urls', namespace='oscm')),
    url(r'^admin/', include(admin.site.urls)),
)

handler404 = 'oscm_app.errors.error_views.page_not_found'
handler500 = 'oscm_app.errors.error_views.server_error'
