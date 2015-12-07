from .default import *

from Site.models import *



class LocationFixture(BaseFixture):

	def run(self, index):

		location = Location(
			address=self.random_street(),
			city=self.random_city(),
			state=self.random_state(),
			zip=self.random_zip()
		)

		location.save()


class SocialMediaPhotosFixture(BaseFixture):

	base_string = "http://lorempixel.com/{0}/{0}/"

	def run(self, index):
		url = self.base_string.format(250-index,250-index)
		instance = SocialMediaPhotos(image=url, thumb=url)
		instance.save()