import hashlib
import io
import urllib
import sys
import urllib.request

from PIL import Image
from commands.decorators import Singleton
from django.core.files.uploadedfile import SimpleUploadedFile
from django.template.loader import render_to_string
from haystack.query import SearchQuerySet


class ModelBackedService(object):
	model = None


# represents a service that wraps a particular model.
# it exists primarily because django's model and queryset
# api can be rather verbose for simple things.
class RepositoryService(ModelBackedService):
	@classmethod
	def find(cls, pk):
		matches = cls.model.objects.filter(pk=pk)
		return matches[0] if matches.exists() else None

	@classmethod
	def get(cls, pk):
		return cls.model.objects.get(pk=pk)


# a service mixin that allows searching of haystack indices
class IndexService(ModelBackedService):
	@classmethod
	def query(cls, query):
		return SearchQuerySet().models(cls.model).load_all().auto_query(query)

	@classmethod
	def query_objects(cls, query, page_size=sys.maxsize):
		search_results = cls.query(query)[:page_size]
		results = [(result.score, result.object) for result in search_results if result is not None]
		sorted(results, key=lambda result: result[0])
		return [result[1] for result in results]


class ImageService(object):
	filename = 'img.jpg'
	facebook_base_url = "http://graph.facebook.com/{0}/picture?width={1}&height={2}"
	gravatar_base_url = "http://www.gravatar.com/avatar/{0}?s={1}d=404"

	@classmethod
	def image_from_url(cls, url):
		stream = urllib.request.urlopen(url)

		if stream.getcode() == 404:
			return None

		bytes = io.BytesIO(stream.read())
		image = Image.open(bytes)
		storage = io.BytesIO()
		image.save(storage, 'jpeg', quality=100)
		storage.seek(0)
		return SimpleUploadedFile(cls.filename, storage.read(), content_type='image/jpeg')

	@classmethod
	def facebook_image(cls, uid, width=400, height=400):
		request_url = cls.facebook_base_url.format(uid, width, height)
		return cls.image_from_url(request_url)

	@classmethod
	def gravatar_image(cls, email, size=400):
		request_url = cls.gravatar_base_url.format(hashlib.md5(email.encode('UTF-8')).hexdigest(), size)
		return cls.image_from_url(request_url)


class NotificationInterface(object):
	# TODO
	def send(self, message, target):
		print(message)

	# TODO
	def bulk_send(self, message, targets):
		print(message)

	def notify_of_game_start_and_assignment(self, game, assignment):
		raise NotImplementedError

	def notify_of_new_assignment(self, game, assignment):
		raise NotImplementedError

	def notify_hosts_of_game_start(self, game, hosts):
		raise NotImplementedError


@Singleton
class EmailService(NotificationInterface):
	templates = {
		'game_start_and_assignment': 'emails/game_start_and_assignment.html',
		'game_start_hosts': 'email/game_start_hosts.html',
		'assignment': 'emails/assignment.html'
	}

	def notify_of_game_start_and_assignment(self, game, assignment):
		template = self.templates['game_start_and_assignment']
		contents = render_to_string(template, {'game': game, 'assignment': assignment})
		self.send(contents, assignment.killer.email)

	def notify_of_new_assignment(self, game, assignment):
		template = self.templates['game_start_hosts']
		contents = render_to_string(template, {'game': game, 'assignment': assignment})
		self.send(contents, assignment.killer.email)

	def notify_hosts_of_game_start(self, game, hosts):
		template = self.templates['game_start_hosts']
		contents = render_to_string(template, {'game': game})
		self.bulk_send(contents, [host.email for host in hosts])


@Singleton
class SMSService(NotificationInterface):
	templates = {
		'game_start_and_assignment': 'sms/game_start_and_assignment.html',
		'game_start_hosts': 'sms/game_start_hosts.html',
		'assignment': 'sms/assignment.html'
	}

	def notify_of_game_start_and_assignment(self, game, assignment):
		template = self.templates['game_start_and_assignment']
		contents = render_to_string(template, {'game': game, 'assignment': assignment})
		self.send(contents, assignment.killer.profile.phone)

	def notify_hosts_of_game_start(self, game, hosts):
		template = self.templates['game_start_hosts']
		contents = render_to_string(template, {'game': game})
		self.bulk_send(contents, [host.profile.phone for host in hosts])

	def notify_of_new_assignment(self, game, assignment):
		template = self.templates['assignment']
		contents = render_to_string(template, {'assignment': assignment, 'game': game})
		self.send(contents, assignment.killer.profile.phone)


@Singleton
class NotificationService(object):
	email_service = EmailService()
	sms_service = SMSService()

	def send_message_to_game(self, game, message, send_emails, send_texts):

		if send_emails:
			email_addresses = [user.email for user in game.associated_users if user.profile.should_email]
			self.email_service.bulk_send(message, email_addresses)

		if send_texts:
			phone_numbers = [user.profile.phone for user in game.associated_users if user.profile.should_text]
			self.sms_service.bulk_send(message, phone_numbers)

	def notify_of_game_start_and_assignment(self, game, assignment):
		user = assignment.killer
		profile = user.profile

		if profile.should_email:
			self.email_service.notify_of_game_start_and_assignment(game, assignment)

		if profile.should_text:
			self.sms_service.notify_of_game_start_and_assignment(game, assignment)

	def notify_of_new_assignment(self, game, assignment):

		user = assignment.killer
		profile = user.profile

		if profile.should_email:
			self.email_service.notify_of_new_assignment(game, assignment)

		if profile.should_text:
			self.sms_service.notify_of_new_assignment(game, assignment)

	def notify_hosts_of_game_start(self, game):
		hosts_to_email = filter(lambda host: host.profile.should_email, game.hosts)
		hosts_to_text = filter(lambda host: host.profile.should_text, game.hosts)

		self.email_service.notify_hosts_of_game_start(game, hosts_to_email)
		self.sms_service.notify_hosts_of_game_start(game, hosts_to_text)
