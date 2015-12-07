from django.shortcuts import render
from django.views.generic import TemplateView, FormView

from Game.forms import GameCreationForm
from Site.app import SiteAppConfig
from .models import *
from .game_service import GameService

game_service = GameService()


def merge(*dict_args):
	result = {}
	for dictionary in dict_args:
		result.update(dictionary)
	return result


def get_game_context(pk): return {'game': game_service.find(pk)}


class CreateGame(FormView):
	form_class = GameCreationForm
	template_name = 'Game/create.html'

	def get_context_data(self, **kwargs):
		public_rules = RuleSet.objects.filter(public=True)

		return {
			'states': SiteAppConfig.STATES,
			'rule_sets': public_rules
		}


class GameSearchList(TemplateView):
	template_name = 'Game/games.html'

	def get_page(self):
		if 'page' in self.request.GET:
			try:
				return int(self.request.GET['page'])
			except TypeError:
				return 1
		else:
			return 1

	def get_query(self):
		if 'query' in self.request.GET:
			return str(self.request.GET['query'])
		else:
			return ''

	def get_context_data(self, **kwargs):
		context = {}
		page = self.get_page()
		query = self.get_query()
		if page > 1: context['page'] = page
		if query != '': context['query'] = query
		return context


class GameView(TemplateView):
	template_name = 'Game/home.html'

	def get_context_data(self, **kwargs):
		return get_game_context(self.kwargs['pk'])


class GameJoin(TemplateView):
	template_name = 'Game/join.html'

	def get(self, request, *args, **kwargs):
		ctx = self.get_context_data(**kwargs)
		game = ctx['game']
		if game and game.open:
			if request.user not in game.associated_users:
				game.users += request.user
				game.save()
				ctx['newly_joined'] = True
			else:
				ctx['already_joined'] = True
		else:
			ctx['available'] = False

		return self.render_to_response(ctx)

	def get_context_data(self, **kwargs):
		return {'game': Game.objects.get(hash=kwargs['hash'])}


class LeaderboardsView(TemplateView):
	template_name = 'Game/leaderboards.html'

	def get_row_for_player_and_assignments(self, player, assignments):
			return {
					'player': player,
					'kills': len([assignment for assignment in assignments
								  if assignment.success and assignment.killer == player]),
					'alive': not any([assignment.success and assignment.killee == player
								 for assignment in assignments])
			}


	def get_context_data(self, **kwargs):
		game = game_service.find(self.kwargs['pk'])
		assignments = game.assignments
		leaderboards = [self.get_row_for_player_and_assignments(player,assignments)
						for player in game.players.all()]
		leaderboards = sorted(leaderboards, key=lambda x: x['kills'], reverse=True)
		return {'game': game, 'leaderboards': leaderboards}


class RulesView(TemplateView):
	template_name = 'Game/rules.html'

	def get_context_data(self, **kwargs):
		return get_game_context(self.kwargs['pk'])


class AnnouncementsView(TemplateView):
	template_name = 'Game/announcements.html'

	def get_context_data(self, **kwargs):
		return get_game_context(self.kwargs['pk'])


class ManagementView(TemplateView):
	template_name = 'Game/management.html'

	def get(self, request, *args, **kwargs):
		return self.respond(request, self.build_context(request, **kwargs))

	def respond(self, request, context):
		game = context['game']
		if game.get_user_is_owner(request.user) or game.get_user_is_reviewer(request.user):
			return render(request, 'Game/management.html', context)
		else:
			# todo
			return render(request, '')

	def build_context(self, request, **kwargs):

		game = game_service.find(kwargs['pk'])

		need_review = [assignment for assignment
					   in game_service.get_pending_assignments(game)
					   if assignment.needs_admin_review]

		pending = [assignment for assignment
				   in game_service.get_pending_assignments(game)
				   if not assignment.needs_admin_review]

		complete = game_service.get_complete_assignments(game)

		incomplete = game_service.get_incomplete_assignments(game)

		return {
			'game': game,
			'complete': complete,
			'pending': pending,
			'review': need_review,
			'incomplete': incomplete,
			'join_url': request.build_absolute_uri(game.join_url),
		}
