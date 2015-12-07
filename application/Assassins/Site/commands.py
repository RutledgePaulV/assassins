from commands.base import *
from django.core.urlresolvers import reverse
from .models import *
import time

class ReverseUrl(CommandHandlerBase):

	command_name = 'REVERSE_URL'

	params = [
		Param('view_name', Types.STRING, True),
		Param('kwargs', Types.OBJECT, False)
	]

	def handle(self, data):

		try:
			path = reverse(data.view_name, kwargs=data.kwargs)
			return self.success(path)
		except:
			return self.error('Could not resolve view name.')


class QueryImage(CommandHandlerBase):

	command_name = 'QUERY_IMAGES'

	params = [Param('size', Types.INTEGER, False, 10)]

	def handle(self, data):
		images = SocialMediaPhotos.objects.all()[:data.size]
		return self.success({'images':[image.dictify for image in images]})


class PingServer(CommandHandlerBase):

	command_name = 'PING'

	def handle(self, data):
		return self.success({'currentDate': time.strftime('%m/%d/%Y %I:%M %p')})