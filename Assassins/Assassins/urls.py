from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


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
        url(r'^500/$', 'django.views.defaults.server_error'),
        url(r'^404/$', 'django.views.defaults.page_not_found'),
		url(r'^403/$', 'django.views.defaults.permission_denied'),
		url(r'^400/$', 'django.views.defaults.bad_request'),
    ]