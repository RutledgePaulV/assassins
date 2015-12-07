from enum import Enum
from django.apps import AppConfig


class GameAppConfig(AppConfig):
	name = 'Game'

	STATUSES = (
		('F', 'Failed'),
		('S', 'Success'),
		('I', 'Incomplete'),
		('P', 'Pending'),
	)


	FAILED=STATUSES[0][0]
	SUCCESS=STATUSES[1][0]
	INCOMPLETE=STATUSES[2][0]
	PENDING=STATUSES[3][0]