from django.forms import ModelForm
from Site.models import *


class LocationForm(ModelForm):

	class Meta:
		model = Location
		fields = ('address', 'state', 'city', 'zip')