from django.core.urlresolvers import reverse
from django.db import models
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import *
from Site.models import *
from Helpers.images import *
import os
import hashlib

class Member(AbstractBaseUser, PermissionsMixin):

	objects = MemberManager()
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ('first_name', 'last_name')

	email = models.EmailField(unique=True)
	first_name = models.CharField(max_length=256)
	last_name = models.CharField(max_length=256)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	profile = models.OneToOneField('Profile')

	def has_module_perms(self, app_label):
		return self.is_admin or super(Member, self).has_module_perms(app_label)

	def has_perm(self, perm, obj=None):
		return self.is_admin or super(Member, self).has_perm(perm, obj)

	def has_perms(self, perm_list, obj=None):
		return self.is_admin or super(Member, self).has_perms(perm_list, obj)

	@property
	def is_staff(self):
		return self.is_admin

	def get_full_name(self):
		return '{0} {1}'.format(self.first_name, self.last_name)

	def get_short_name(self):
		return self.first_name

	def __str__(self):
		return self.get_full_name()

	@property
	def hash_key(self):
		encoded = str(self.email).encode('utf-8')
		return hashlib.sha224(encoded).hexdigest()

	@property
	def link(self):
		return reverse('users:view_profile', kwargs={'pk': self.pk})

	@property
	def dictify(self):
		return {
			'pk': self.pk,
			'first_name':self.first_name,
			'last_name': self.last_name,
			'email': self.email,
			'last_login': {
				'month': self.last_login.month,
				'day': self.last_login.day,
				'year': self.last_login.year
			} if self.last_login else None
		}

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if not hasattr(self, 'profile'):
			p = Profile()
			p.save()
			self.profile = p
		return super(Member, self).save(force_insert, force_update, using, update_fields)



class Profile(models.Model):

	should_email = models.BooleanField(default=True)
	should_text = models.BooleanField(default=False)
	phone = models.CharField(max_length=255, blank=True, null=True)
	slogan = models.CharField(max_length=255, blank=True, null=True)
	biography = models.TextField(max_length=1024, blank=True, null=True)
	image = models.ImageField(upload_to='profile_pictures', blank=True, null=True)
	thumb = models.ImageField(upload_to='profile_pictures/thumbs', blank=True, null=True)

	def __str__(self):
		return str(self.member)

	@property
	def image_url(self):
		if self.image and self.image.url:
			return self.image.url
		else:
			return static('images/silhouette.jpg')

	@property
	def thumb_url(self):
		if self.thumb and self.thumb.url:
			return self.thumb.url
		else:
			return static('images/thumbs/silhouette.jpg')

	@property
	def dictify(self):
		results = {}

		results['image'] = self.image_url
		results['thumb'] = self.thumb_url
		results['phone'] = self.phone if self.phone else None

		return results

	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		if self.image:
			extension = os.path.split(self.image.name)[-1]
			filename = "{0}.{1}".format(self.member.hash_key, extension)
			image, thumb = resize_image(self.image, (400, 400), (200, 200), filename)
			self.image.save(filename, image, save=False)
			self.thumb.save(filename, thumb, save=False)
		super(Profile, self).save(force_insert, force_update, using, update_fields)