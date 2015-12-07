from Game.app import GameAppConfig
from Game.game_service import GameService
from Game.models import Assignment, Game
from .default import *

game_service = GameService()

class AssignmentsFixture(BaseFixture):

	def run(self, index):
		[game_service.start_game(game) for game in Game.objects.all()]

