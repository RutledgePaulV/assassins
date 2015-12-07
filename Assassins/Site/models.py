from django.db import models
from Site.app import SiteAppConfig
from Helpers.images import *
import os


class SocialMediaPhotos(models.Model):

	date_created = models.DateTimeField(auto_now_add=True)

	image = models.URLField()
	thumb = models.URLField(blank=True, null=True)


	@property
	def dictify(self):
		return {
			'image':self.image,
			'thumb':self.thumb
		}


class Location(models.Model):

	address = models.CharField(max_length=255)
	state = models.CharField(max_length=128, choices=SiteAppConfig.STATES)
	city = models.CharField(max_length=255)
	zip = models.CharField(max_length=5)

	@classmethod
	def validate_state(cls, state):
		abbreviations = [data[0] for data in SiteAppConfig.STATES]
		return state in abbreviations

	@property
	def dictify(self):
		return {
			'address': self.address,
			'state': self.state,
			'city': self.city,
			'zip': self.zip
		}

	def __str__(self):
		return "{0}\n{1}, {2} {3}".format(self.address, self.city, self.state, self.zip)