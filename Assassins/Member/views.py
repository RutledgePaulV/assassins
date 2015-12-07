from django.db.models import Q

from django.views.generic import TemplateView

from Member.models import Member
from Game.models import *


class ProfileView(TemplateView):
	template_name = 'Member/profile.html'


class OtherProfileView(TemplateView):
	template_name = 'Member/view_profile.html'

	def get_context_data(self, **kwargs):
		users = Member.objects.filter(pk=kwargs['pk'])
		return {'other_user': users[0]} if users.exists() else {}


class GamesView(TemplateView):
	template_name = 'Member/games.html'

	def get_filter(self):
		return Q(players=self.request.user) | Q(reviewers=self.request.user) | Q(owner=self.request.user)

	def get_context_data(self, **kwargs):
		filter_object = self.get_filter()
		return {'games': Game.objects.filter(filter_object)}


class AssignmentsView(TemplateView):
	template_name = 'Member/assignments.html'

	def organize_by_game(self, assignments):
		grouped_by_games = {}
		for assignment in assignments:
			if assignment.game.pk not in grouped_by_games:
				grouped_by_games[assignment.game.pk] = {'assignments': [assignment]}
			else:
				grouped_by_games[assignment.game.pk]['assignments'].append(assignment)

		return {'games': list(grouped_by_games.values())}

	def get_context_data(self, **kwargs):
		return self.organize_by_game(Assignment.objects.filter(killer=self.request.user))