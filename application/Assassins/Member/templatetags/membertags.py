from django import template

register = template.Library()
from Member.models import Member
from Member.service import MemberService

member_service = MemberService()

@register.filter(name='is_coparticipant')
def is_coparticipant(user1, user2):
	if isinstance(user1, Member) and isinstance(user2, Member):
		return member_service.users_are_coparticipants(user1, user2)
	else:
		return False