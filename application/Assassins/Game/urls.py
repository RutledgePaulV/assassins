from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from Game.views import *


urlpatterns = [
	# no special requirements to view the landing page of a game
	url(r'^(?P<pk>\d+)/$', GameView.as_view(), name='view'),

	# no special requirements to view the list of all games.
	url(r'^$', GameSearchList.as_view(), name='list'),

	# you must have an account to create a game
	url(r'^create/$', login_required(CreateGame.as_view()), name='create'),

	# these are protected to only members of a game
	url(r'^(?P<pk>\d+)/leaderboards/$', login_required(LeaderboardsView.as_view()), name='leaderboards'),
	url(r'^(?P<pk>\d+)/rules/$', login_required(RulesView.as_view()), name='rules'),
	url(r'^(?P<pk>\d+)/news/$', login_required(AnnouncementsView.as_view()), name='news'),
	url(r'^(?P<pk>\d+)/manage/$', login_required(ManagementView.as_view()), name='manage'),
	url(r'^join/(?P<hash>.*)/$', login_required(GameJoin.as_view()), name='join'),
]