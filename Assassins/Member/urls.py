from django.conf.urls import url
from django.contrib.auth.views import *

from .views import *


urlpatterns = [
	url(r'^(?P<pk>\d+)/$', login_required(OtherProfileView.as_view()), name='view_profile'),
	url(r'^profile/$', login_required(ProfileView.as_view()), name='profile'),
	url(r'^games/$', login_required(GamesView.as_view()), name='games'),
	url(r'^assignments/$', login_required(AssignmentsView.as_view()), name='assignments')
]
