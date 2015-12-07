from commands.decorators import Singleton
from Game.models import *
from django.db.models import Q
from Helpers.services import RepositoryService, IndexService
from Member.models import Member


@Singleton
class MemberService(RepositoryService, IndexService):

	model = Member

	@classmethod
	def users_are_coparticipants(cls, user1, user2):

		# this method checks to see if there are any games that these two
		# users are both involved with. If there are, then they are permitted
		# to view each others profiles
		contains_user_1 = Q(reviewers__in=[user1]) | Q(players__in=[user1]) | Q(owner=user1)
		contains_user_2 = Q(reviewers__in=[user2]) | Q(players__in=[user2]) | Q(owner=user2)
		complete_q = contains_user_1 & contains_user_2

		return Game.objects.filter(complete_q).exists()

