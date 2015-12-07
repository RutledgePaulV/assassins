from .base import *

# the hosts we need to allow access to the application
ALLOWED_HOSTS = ['*']

# telling compress to use the less precompiler for less files and handlebars templates
COMPRESS_PRECOMPILERS = (
	('text/less', '/usr/local/bin/lessc -x {infile}'),
)

# the relative folder where media and static resources should be collected
MEDIA_ROOT = os.path.join(BASE_DIR, 'serve_media')
STATIC_ROOT = os.path.join(BASE_DIR, 'serve_static')
COMPRESS_ROOT = STATIC_ROOT

# we'll always want to be in debug mode when running locally
TEMPLATE_DEBUG = DEBUG = REQUIRE_DEBUG = True
COMPRESS_ENABLED = False

# database connection details
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
	}
}

HAYSTACK_CONNECTIONS = {
	'default': {
		'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
		'PATH': os.path.join(BASE_DIR, 'whoosh'),
	},
}

# it's fine to hardcode the secret key locally, but we'll read it from an env variable in prod
SECRET_KEY = '$$5+&zvh8*vtl895^g-qv7$#usbmmd2g^8&!%ng)i1t^4@i@h!'

# console backend for debugging
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# site id
SITE_ID = 3

# rabbit mq
BROKER_URL = 'amqp://localhost:5672/'

HEAP_TOKEN = "1953287414"