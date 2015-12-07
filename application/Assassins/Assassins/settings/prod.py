from .base import *

# the hosts we need to allow access to the application
ALLOWED_HOSTS = ['assassins.io']

# telling compress to use the less precompiler for less files and handlebars templates
COMPRESS_PRECOMPILERS = (
	('text/less', '/usr/local/bin/lessc -x {infile}'),
)

# the relative folder where media and static resources should be collected
MEDIA_ROOT = os.environ['MEDIA_ROOT']
STATIC_ROOT = os.environ['STATIC_ROOT']
COMPRESS_ROOT = STATIC_ROOT

# in production we want to compress everything and run nothing in debug mode
COMPRESS_ENABLED = True
TEMPLATE_DEBUG = DEBUG = REQUIRE_DEBUG = False

# database connection details
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql_psycopg2',
		'NAME': os.environ['DB_NAME'],
		'USER': os.environ['DB_USER'],
		'PASSWORD': os.environ['DB_PASS'],
		'HOST': os.environ['DB_HOST'],
		'PORT': os.environ['DB_PORT']
	}
}

# in production we want a persistent whoosh index so it's maintained across restarts
HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH': os.environ['WHOOSH_ROOT']
	}
}

# reading the secret key on the server from an ENV variable
SECRET_KEY = os.environ['SECRET_KEY']

# our site id
SITE_ID = 3

HEAP_TOKEN = "2904959477"

# rabbit mq
BROKER_URL = 'amqp://{0}:{1}@{2}:{3}/'.format(
	os.environ['MQ_USER'],
	os.environ['MQ_PASS'],
	os.environ['MQ_HOST'],
	os.environ['MQ_PORT']
)