from commands.base import *
from commands.decorators import *
from haystack.utils import Highlighter

from Helpers.services import NotificationService
from Member.models import Member
from Member.service import MemberService
from Site.app import SiteAppConfig
from Site.models import Location
from .models import *
from .game_service import GameService

notification_service = NotificationService()
game_service = GameService()
member_service = MemberService()


class Search(CommandHandlerBase):
	command_name = 'SEARCH_GAMES'

	params = [
		Param('query', Types.STRING),
		Param('page', Types.INTEGER),
	]

	PAGE_SIZE = 25

	@staticmethod
	def build_results_for_page(games, query):
		highlighter = Highlighter(query)

		return [{'url': game.url,
		         'title': highlighter.highlight(game.title),
		         'intro': highlighter.highlight(game.intro),
		         'city': highlighter.highlight(game.location.city),
		         'state': highlighter.highlight(game.location.state)} for game in games]

	@staticmethod
	def build_meta(query, page_number):
		return {
			'query': query,
			'page': page_number,
		}

	def handle(self, data):

		query = data.query
		funnel = None

		if self.user:
			query, funnel = self.get_funnel(query)

		games = game_service.query_objects(query, self.PAGE_SIZE)

		if funnel:
			games = funnel(games)

		results = self.build_results_for_page(games, data.query)
		meta = self.build_meta(data.query, 1)
		return self.success(results, meta)

	def get_funnel(self, query):
		if query == ':player':
			return '', lambda games: filter(lambda game: game.get_user_is_player(self.user), games)
		elif query == ':reviewer':
			return '', lambda games: filter(lambda game: game.get_user_is_reviewer(self.user), games)
		elif query == ':owner':
			return '', lambda games: filter(lambda game: game.get_user_is_owner(self.user), games)
		else:
			return query, None

	@normalizer('query')
	def normalize_query(self, query):
		return query.strip().lower()


class CreateGame(CommandHandlerBase):
	command_name = 'CREATE_GAME'

	auth_required = True

	params = [
		Param('title', Types.STRING),
		Param('intro', Types.STRING),
		Param('address', Types.STRING),
		Param('city', Types.STRING),
		Param('state', Types.STRING),
		Param('zip', Types.STRING),
		Param('start_date', Types.STRING),
		Param('rules_pk', Types.INTEGER)
	]

	@normalizer('city')
	def normalize_city(self, city):
		return city.strip().title()

	@normalizer('state')
	def normalize_state(self, state):
		return state.strip().upper()

	@normalizer('address')
	def normalize_address(self, address):
		return address.strip()

	@validator('state', 'The provided state does not match the required format.')
	def validate_state(self, state):
		return state in SiteAppConfig.STATE_ABBREVIATIONS

	@validator('rules_pk', 'The provided primary key for a rule set does not correspond to an existing rule set.')
	def validate_rules_pk(self, rules_pk):
		return RuleSet.objects.filter(pk=rules_pk).exists()

	def handle(self, data):

		# construct a location model based on the provided information
		location = Location(address=data.address, city=data.city, state=data.state, zip=data.zip)
		location.save()

		# get their base rule set and then create private copy for their instance
		base_rule_set = RuleSet.objects.get(pk=data.rules_pk)

		game = Game(title=data.title,
		            intro=data.intro,
		            location=location,
		            rules=base_rule_set,
		            start_date=data.start_date
		            )

		try:
			game.owner = self.user
			game.save()
			return self.success({'message': 'Game created successfully'})
		except Exception as e:
			return self.error(str(e))


class UserList(CommandHandlerBase):
	command_name = 'LIST_USERS_FOR_GAME'

	params = [
		Param('pk', Types.INTEGER),
		Param('type', Types.STRING, False, 'ALL'),
		Param('query', Types.STRING, False),
	]

	auth_required = True

	@validator('pk', 'Game does not exist.', order=0)
	def validate_and_fetch_game(self, pk):
		game = game_service.find(pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('user', 'User is not a participant in the game and therefore cannot query the users.', order=1)
	def user_is_co_participant(self, user):
		return user in self.game.associated_users

	@normalizer('type')
	def normalize_to_uppercase(self, type):
		return type.strip().upper()

	def handle(self, data):

		game = self.game

		results = member_service.query_objects(data.query)

		if data.type == 'REVIEWERS':
			results = filter(lambda member: game.get_user_is_reviewer(member), results)
		elif data.type == 'PLAYERS':
			results = filter(lambda member: game.get_user_is_player(member), results)

		return self.success([self.build_result_for_user(member) for member in results])

	def build_result_for_user(self, user):
		user_dict = user.dictify
		profile_dict = user.profile.dictify
		user_dict.update({'kills': self.game.get_kill_count(user)})
		user_dict.update(profile_dict)
		return user_dict


class MakeReviewer(CommandHandlerBase):
	command_name = 'MAKE_REVIEWER'

	auth_required = True

	params = [
		Param('game', Types.INTEGER),
		Param('player_pk', Types.INTEGER)
	]

	@validator('game', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, pk):
		game = game_service.find(pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('player_pk', 'The player is not eligible to made an owner of this game.', order=1)
	def validate_player_is_in_game(self, pk):
		player = Member.objects.filter(pk=pk)
		if player.exists:
			self.player = player[0]
			return self.game.get_user_is_player(self.player)
		return False

	@validator('user', 'The user does not have the necessary permissions to kick people from the game', order=2)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_owner(user)

	def handle(self, data):

		self.game.players.remove(self.player)
		self.game.reviewers.add(self.player)
		self.game.save()

		return self.success({}, {'message': 'Reviewer added successfully'})


class MakeOwner(CommandHandlerBase):
	command_name = 'MAKE_OWNER'

	auth_required = True

	params = [
		Param('game', Types.INTEGER),
		Param('player_pk', Types.INTEGER)
	]

	@validator('game', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, pk):
		game = game_service.find(pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('player_pk', 'The player is not eligible to made an owner of this game.', order=1)
	def validate_player_is_in_game(self, pk):
		player = Member.objects.filter(pk=pk)
		if player.exists:
			self.player = player[0]
			return self.game.get_user_is_reviewer(self.player)
		return False

	@validator('user', 'The user does not have the necessary permissions to kick people from the game', order=2)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_owner(user)

	def handle(self, data):

		self.game.owner = self.player
		self.game.reviewers.remove(self.player)
		self.game.reviewers.add(self.user)
		self.game.save()

		return self.success({}, {'message': 'Owner changed successfully.'})


class KickPlayer(CommandHandlerBase):
	command_name = 'KICK_FROM_GAME'

	auth_required = True

	params = [
		Param('game', Types.INTEGER),
		Param('player_pk', Types.INTEGER)
	]

	@validator('game', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, pk):
		game = game_service.find(pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('player_pk', 'The player to be kicked is not part of the game and so cannot be removed.', order=1)
	def validate_player_is_in_game(self, pk):
		player = Member.objects.filter(pk=pk)
		if player.exists:
			self.player = player[0]
			return self.game.get_user_is_associated(self.player)
		return False

	@validator('user', 'The user does not have the necessary permissions to kick people from the game', order=2)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_reviewer(user) or self.game.get_user_is_owner(user)

	def handle(self, data):

		player = self.player

		is_reviewer = self.game.get_user_is_reviewer(player)

		if is_reviewer and not self.game.get_user_is_owner(self.user):
			return self.error('Only owner\'s of a game can kick reviewers.')

		if is_reviewer:
			self.game.reviewers.remove(player)
		else:
			self.game.players.remove(player)

		self.game.save()

		return self.success({}, meta={'message': 'User was successfully removed from the game.'})


class UpdateGameRules(CommandHandlerBase):
	command_name = 'UPDATE_GAME_RULES'

	params = [
		Param('pk', Types.INTEGER),
		Param('html', Types.STRING)
	]

	auth_required = True

	@validator('pk', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, pk):
		game = game_service.find(pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('user', 'The user does not have the necessary permissions to update the game\'s rule set', order=1)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_reviewer(user)

	def handle(self, data):
		rules = self.game.rules
		rules.html = data.html
		rules.save()

		return self.success({'message': 'The save was successful.'})


class PostNotification(CommandHandlerBase):
	command_name = 'POST_NOTIFICATION'

	auth_required = True

	params = [
		Param('pk', Types.INTEGER),
		Param('subject', Types.STRING),
		Param('contents', Types.STRING),
		Param('send_email', Types.BOOLEAN, False),
		Param('send_text', Types.BOOLEAN, False)
	]

	@validator('pk', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, pk):
		game = game_service.find(pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('user', 'The user does not have the necessary permissions to update the game\'s rule set', order=1)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_reviewer(user)

	def handle(self, data):

		announcement = Announcement(
			game=self.game,
			author=self.user,
			subject=data.subject,
			html=data.contents,
		)

		announcement.save()

		notification_service.send_message_to_game(self.game, data.contents, data.send_email, data.send_text)

		return self.success({'message': 'Announcement created successfully.'})


class GetManagementSection(CommandHandlerBase):
	command_name = 'GET_MANAGEMENT_SECTION'

	auth_required = True

	params = [
		Param('game', Types.INTEGER),
		Param('type', Types.STRING)
	]

	@validator('game', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, game_pk):
		game = game_service.find(game_pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('user', 'The user does not have sufficient permissions to management information', order=1)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_reviewer(user)

	@validator('type', 'The provided type does not match one of the expected cases.')
	def validate_type(self, review_type):
		return review_type in ('admin_review', 'other_review', 'incomplete', 'complete')

	def handle(self, data):

		results = []

		if data.type == 'admin_review':
			results = [result.dictify for result
			           in game_service.get_pending_assignments(self.game)
			           if result.needs_admin_review]

		elif data.type == 'other_review':
			results = [result.dictify for result
			           in game_service.get_pending_assignments(self.game)
			           if not result.needs_admin_review]

		elif data.type == 'incomplete':
			results = [result.dictify for result
			           in game_service.get_incomplete_assignments(self.game)]

		elif data.type == 'complete':
			results = [result.dictify for result
			           in game_service.get_complete_assignments(self.game)]

		return self.success(results, {'count': len(results)})


class AssignmentReportStatus(CommandHandlerBase):
	command_name = 'ASSIGNMENT_REPORT_STATUS'

	auth_required = True

	params = [
		Param('assignment', Types.INTEGER),
		Param('verdict', Types.BOOLEAN)
	]

	@validator('assignment', 'The provided primary key does not match an existing assignment.', order=0)
	def validate_and_fetch_game(self, assignment_pk):
		assignments = Assignment.objects.filter(pk=assignment_pk)
		if assignments.exists():
			self.assignment = assignments[0]
			return True
		else:
			return False

	@validator('user', 'The user does not have a necessary relationship to submit their status for this assignment',
	           order=1)
	def validate_user_permissions(self, user):
		self.is_killer = user == self.assignment.killer
		self.is_killee = user == self.assignment.killee
		self.is_admin = self.assignment.game.get_user_is_reviewer(user)
		return any((self.is_killer, self.is_killee, self.is_admin))

	def handle(self, data):

		assignment = self.assignment

		if self.is_killer:
			assignment.killer_verdict = data.verdict
		elif self.is_killee:
			assignment.killee_verdict = data.verdict
		elif self.is_admin:
			assignment.admin_verdict = data.verdict

		assignment.save()

		return self.success({}, meta={'message': 'Verdict successfully marked.'})


class DeleteGame(CommandHandlerBase):
	command_name = 'DELETE_GAME'

	auth_required = True

	params = [Param('game', Types.INTEGER)]

	@validator('game', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, game_pk):
		game = game_service.find(game_pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('user', 'The user does not have sufficient permissions to delete the game.', order=1)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_owner(user)

	def handle(self, data):

		try:
			self.game.delete()
			return self.success({}, meta={'confirmed': True})
		except:
			return self.error('Game could not be deleted.')


class ToggleRegistration(CommandHandlerBase):
	command_name = 'TOGGLE_REGISTRATION'

	auth_required = True

	params = [
		Param('game', Types.INTEGER),
		Param('open', Types.BOOLEAN)
	]

	@validator('game', 'The provided primary key does not match an existing game.', order=0)
	def validate_and_fetch_game(self, game_pk):
		game = game_service.find(game_pk)
		if game:
			self.game = game
			return True
		else:
			return False

	@validator('user', 'The user does not have sufficient permissions to toggle registration.', order=1)
	def validate_user_permissions(self, user):
		return self.game.get_user_is_owner(user)

	def handle(self, data):

		if self.game.open != data.open:
			self.game.open = data.open
			self.game.save()
			return self.success({}, meta={'success': True})
		else:
			return self.error('Registration for game is already {0}'.format(self.game.open))
