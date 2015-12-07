from commands.decorators import Singleton
from haystack.query import SearchQuerySet
from .models import *
from Helpers.services import *
from Helpers.services import NotificationService
from datetime import datetime
import random

notification_service = NotificationService()

def generate_assignments(game):
	users = list(game.players.all())
	random.shuffle(users)

	for x in range(0, len(users)):

		# next user in the list if exists, otherwise we want the first user
		y = x + 1 if x+1 < len(users) else 0

		user1 = users[x]
		user2 = users[y]

		assignment = Assignment(killer=user1, killee=user2, game=game)

		assignment.save()


def update_game_properties(game):
	game.in_progress = True

def send_assignment_notifications(game):
	map(lambda assignment:
		notification_service.notify_of_game_start_and_assignment(game, assignment), game.assignments)

def send_host_notifications(game):
	notification_service.notify_hosts_of_game_start(game)


@Singleton
class GameService(RepositoryService, IndexService):

	model = Game

	@classmethod
	def get_pending_games(cls):
		return Game.objects.filter(start_date__lte=datetime.now(), in_progress=False)

	@classmethod
	def start_game(cls, game):
		update_game_properties(game)
		generate_assignments(game)
		send_assignment_notifications(game)
		game.save()

	@classmethod
	def get_complete_assignments(cls, game):
		return Assignment.objects.filter(game=game, status__in=[GameAppConfig.SUCCESS, GameAppConfig.FAILED])

	@classmethod
	def get_pending_assignments(cls, game):
		return Assignment.objects.filter(game=game, status=GameAppConfig.PENDING)

	@classmethod
	def get_incomplete_assignments(cls, game):
		return Assignment.objects.filter(game=game, status=GameAppConfig.INCOMPLETE)
