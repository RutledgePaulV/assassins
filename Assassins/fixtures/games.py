from Site.models import Location
from .default import *
from Game.models import *


class RulesFixture(BaseFixture):

	def run(self, index):
		r = RuleSet(public=True,
					name=self.random_word(),
					html=self.random_html(),
					icon_class=self.random_icon_class()
					)
		r.save()


class GameFixture(BaseFixture):

	max_rand=100

	def run(self, index):
		location = self.random_model(Location)
		rules = self.random_model(RuleSet)

		g = Game(
			title=self.random_word(),
			intro=self.random_block(self.random_number()),
			location=location,
			rules=rules,
			start_date=self.random_date_in_future(datetime.timedelta(days=4))
		)

		users = self.random_users(10)
		g.owner = users.pop()

		g.save()

		for user in range(3):
			g.reviewers.add(users.pop())

		while len(users) != 0:
			g.players.add(users.pop())

		g.save()