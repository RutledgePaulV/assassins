from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.views.defaults import server_error, page_not_found, permission_denied, bad_request

urlpatterns = [
	url(r'', include('Site.urls', namespace='site', app_name='Site')),
	url(r'^games/', include('Game.urls', namespace='games', app_name='Game')),
	url(r'^accounts/', include('allauth.urls')),
	url(r'^users/', include('Member.urls', namespace='users', app_name='Member')),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^commands/', include('commands.urls', namespace='commands')),
]


'''
if in development, we'll have django serve the media files
but in production this will be handled by nginx. We also
want to provide a way to test error pages without having
to flip out of debug mode.
'''
if settings.DEBUG:
	from django.conf.urls.static import static
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += [
        url(r'^500/$', server_error),
        url(r'^404/$', page_not_found),
		url(r'^403/$', permission_denied),
		url(r'^400/$', bad_request),
    ]