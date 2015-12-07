from django.contrib.auth.models import BaseUserManager
from .models import *

class MemberManager(BaseUserManager):

	def create_user(self, email, first_name, last_name, password=None):

		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
			email=self.normalize_email(email),
			first_name = first_name,
			last_name = last_name
		)

		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, first_name, last_name, password):

		user = self.create_user(email, first_name, last_name, password)
		user.is_admin = True
		user.save()
		return user