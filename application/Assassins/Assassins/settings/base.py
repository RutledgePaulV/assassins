# we need access to OS details for creating paths and reading environment variables
import os
from datetime import timedelta

# the base directory for the application.
from django.core.urlresolvers import reverse_lazy

# getting the base directory for the entire webapp
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


# our authentication backends
AUTHENTICATION_BACKENDS = (
	"django.contrib.auth.backends.ModelBackend",
	"allauth.account.auth_backends.AuthenticationBackend"
)


# the middleware we will use for the app
MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
)


# list of applications to load
INSTALLED_APPS = (
	# for some unknown reason, allauth requires sites.
	'django.contrib.sites',

	# standard django apps
	'django_admin_bootstrapped',
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	# haystack for providing free text search and highlighting
	'haystack',

	# all auth for registering and logging in via social accounts
	'allauth',
	'allauth.account',
	'allauth.socialaccount',
	'allauth.socialaccount.providers.facebook',

	# compressor for compiling less
	'compressor',

	# require for optimizing and minifying requirejs modules
	'require',

	# commands for simple AJAX
	'commands',

	# assassins's modules
	'Site',
	'Member',
	'Game',
)


# all of the configuration for django-allauth
SOCIALACCOUNT_QUERY_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_SESSION_REMEMBER = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_ADAPTER = 'Member.adapters.MemberAccountAdapter'
SOCIALACCOUNT_ADAPTER = 'Member.adapters.MemberSocialAccountAdapter'
ACCOUNT_FORMS = {
	'signup': 'Member.forms.MemberCreationForm'
}

SOCIALACCOUNT_FORMS = {
	'signup': 'Member.forms.SocialSignupForm'
}

SOCIALACCOUNT_PROVIDERS = {
	'facebook': {
		'METHOD': 'oauth2',
		'SCOPE': ['email'],
		'VERIFIED_EMAIL': False,
		'VERSION': 'v2.3'
	},
	'google': {
		'SCOPE': ['profile', 'email'],
		'AUTH_PARAMS': {'access_type': 'online'}
	}
}


# configuration for django-require
STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'


# how static files should be loaded
STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
)


# adding the global static directory to the url resolution
# though we keep bower_components inside static, we want to
# expose them one directory higher
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, 'static'),
	os.path.join(BASE_DIR, 'static/bower_components'),
)


# template engine configuration
TEMPLATES = [{
	'BACKEND': 'django.template.backends.django.DjangoTemplates',
	'DIRS': [
		os.path.join(BASE_DIR, 'templates'),
	],
	'OPTIONS': {
		'context_processors': [
			'Assassins.settings.context.compress',
			'django.contrib.auth.context_processors.auth',
			'django.template.context_processors.debug',
			'django.template.context_processors.i18n',
			'django.template.context_processors.media',
			'django.template.context_processors.static',
			'django.template.context_processors.tz',
			'django.template.context_processors.request',
			'django.contrib.messages.context_processors.messages',
		],
		'loaders': [
			'django.template.loaders.filesystem.Loader',
			'django.template.loaders.app_directories.Loader',
		]
	},
}]


# our custom user model
AUTH_USER_MODEL = 'Member.Member'


# redirect url after login when there's no next? query param
LOGIN_REDIRECT_URL = reverse_lazy('users:profile')


# have to set internal ips to point to local host in order for compressor to work properly.
INTERNAL_IPS = ('127.0.0.1', 'assassins.io')


# basic configuration
ROOT_URLCONF = 'Assassins.urls'
WSGI_APPLICATION = 'Assassins.wsgi.application'


# time zone, location, and internationalization
TIME_ZONE = 'UTC'
LANGUAGE_CODE = 'en'
USE_I18N = USE_L10N = USE_TZ = True


# this being here allows for real time updating of the search index as models change
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# celery settings
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


# defining from which subfolder inside the compress_url that the compress files should be served from
COMPRESS_OUTPUT_DIR = 'cache'


# defining the filters that css files should be run through in the compression stage
COMPRESS_CSS_FILTERS = [
	'compressor.filters.css_default.CssAbsoluteFilter'
]


# the base urls to be used for media and static content
MEDIA_URL = '/media/'
STATIC_URL = '/static/'
COMPRESS_URL = STATIC_URL

# logging configuration
LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'console': {
			'class': 'logging.StreamHandler',
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
		},
	},
}

CELERYBEAT_SCHEDULE = {
	'debug': {
		'task': 'Assassins.settings.celery.debug_task',
		'schedule': timedelta(seconds=10)
	},
}
