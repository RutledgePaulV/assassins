import random
import urllib.request
import io

from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile

from Member.models import Member
from Site.app import SiteAppConfig
import datetime


class BaseFixture(object):
	max_rand = 20

	lorem_pixel = 'http://lorempixel.com/{0}/{0}/'

	phrases = [
		'Bingo',
		'Ringo',
		'Sinbad',
		'Tin',
		'Ninja',
		'Rowdy',
		'Pistol',
		'Knees',
		'Prissy'
	]

	street_types = [
		'Way',
		'Avenue',
		'Circle',
		'Court',
		'Boulevard',
		'Highway'
	]

	cities = [
		'Chicago',
		'Hollywood',
		'New York',
		'Minneapolis',
		'Beverly Hills',
		'Columbine',
		'New Haven'
	]

	html_nodes = [
		'<p>Gosh, it is so hard not to love really nice markdown.</p>',
		'<div><span>This is a test</span></div>',
		'<h2>Beautiful Markup Says A Lot</h2>',
		'<p>You can call me polly.</p>',
		'<h4>Wow, this is so cool it might make me drool.</h4>'
	]

	domains = [
		'gmail',
		'yahoo',
		'comcast',
		'hotmail',
		'windows'
	]

	first_names = [
		'Paul',
		'David',
		'Eric',
		'Dan',
		'Matt',
		'Grant',
		'Aly',
		'Linley',
		'Kimberly',
		'Nathan',
		'Kelly',
		'Jekyll'
	]

	last_names = [
		'Bridges',
		'Rafters',
		'Castles',
		'Tinkles',
		'Pinky',
		'Young',
		'Rams',
		'England',
		'Flock',
		'Starbuck',
		'Cracker',
		'Kangaroo'
	]

	def random_phone(self):
		return '({0}{1}{2})-{3}{4}{5}-{6}{7}{8}{9}'.format(*range(10))

	def random_date_in_future(self, max_delta):
		now = datetime.datetime.now()
		delta_as_seconds = max_delta.total_seconds()
		random_point = random.randrange(delta_as_seconds)
		return now + datetime.timedelta(seconds=random_point)

	def random_email(self):
		return '{0}.{1}@{2}.com'.format(
			self.random_first_name(),
			self.random_last_name(),
			random.choice(self.domains)
		)

	def random_first_name(self):
		return random.choice(self.first_names)

	def random_last_name(self):
		return random.choice(self.last_names)

	def random_image(self, width=200, height=200):
		stream = urllib.request.urlopen(self.lorem_pixel.format(width, height)).read()
		bytes = io.BytesIO(stream)
		image = Image.open(bytes)
		storage = io.BytesIO()
		image.save(storage, 'jpeg', quality=100)
		storage.seek(0)

		file = SimpleUploadedFile('{0}-{1}-{2}.jpg'.format(
			self.random_number(),
			self.random_number(),
			self.random_word()),
			storage.read(),
			content_type='image/jpeg')

		return file

	def random_icon_class(self):
		return 'ninja-%02d' % random.randint(0, 15)

	def random_html(self):
		return '<div>{0}</div>'.format(''.join(self.random_set(self.html_nodes, 3)))

	def random_set(self, values, size):
		iterable = list(set(values))[:size]
		random.shuffle(iterable)
		return iterable

	def random_boolean(self):
		return random.choice([True, False])

	def random_state(self):
		return random.choice(SiteAppConfig.STATE_ABBREVIATIONS)

	def random_zip(self):
		return ''.join([str(random.randint(0, 9)) for x in range(5)])

	def random_city(self):
		return random.choice(self.cities)

	def random_street(self):
		return '{0} {1}'.format(self.random_word(), random.choice(self.street_types))

	def random_users(self, size):
		users = set()
		while len(users) < size:
			users.add(self.random_user())
		return users

	def random_user(self):
		return self.random_model(Member)

	def random_word(self):
		return random.choice(self.phrases)

	def random_number(self):
		return random.choice(range(self.max_rand))

	def random_block(self, words):
		return ' '.join([self.random_word() for x in range(words)])

	def random_model(self, model):
		return random.choice(model.objects.all())

	def gen(self, number):
		[self.run(x) for x in range(number)]

	def run(self, index):
		raise NotImplementedError