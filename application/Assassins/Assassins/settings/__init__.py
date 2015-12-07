from __future__ import absolute_import
import os
from .base import *
from .context import *
from .require import *

# deciding which environment specific settings file to load based upon the environment variable
if 'ENV' in os.environ and os.environ['ENV'] == 'PRODUCTION':
	from .prod import *
else:
	from .local import *


# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app