from django import template
from Member.models import Member

register = template.Library()
from Game.models import Game


@register.filter(name='is_owner')
def is_owner(game, user):
	if isinstance(game, Game) and isinstance(user, Member):
		return game.get_user_is_owner(user)
	else:
		return False


@register.filter(name='is_reviewer')
def is_reviewer(game, user):
	if isinstance(game, Game) and isinstance(user, Member):
		return game.get_user_is_reviewer(user)
	else:
		return False


@register.filter(name='is_player')
def is_player(game, user):
	if isinstance(game, Game) and isinstance(user, Member):
		return game.get_user_is_player(user)
	else:
		return False


@register.filter(name='is_participant')
def is_participant(game, user):
	if isinstance(game, Game) and isinstance(user, Member):
		return game.get_user_is_associated(user)
	else:
		return False


@register.filter(name='is_alive')
def is_alive(game, user):
	if isinstance(game, Game) and isinstance(user, Member):
		return game.get_is_alive(user)
	else:
		return False


@register.filter(name='kill_count')
def kill_count(game, user):
	if isinstance(game, Game) and isinstance(user, Member):
		return game.get_kill_count(user)
	else:
		return False