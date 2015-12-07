from commands.base import *
from commands.decorators import *
from django.contrib.auth import login, authenticate
from .models import *
from django.core.validators import *

class GetMemberInfo(CommandHandlerBase):

	command_name = 'GET_MEMBER_INFO'

	auth_required = True

	def handle(self, data):
		return self.success(self.user.dictify)


class UpdateMemberInfo(CommandHandlerBase):

	command_name = 'UPDATE_MEMBER_INFO'

	auth_required = True

	params = [
		Param('email', Types.STRING, False),
		Param('first_name', Types.STRING, False),
		Param('last_name', Types.STRING, False)
	]

	def handle(self, data):

		member = self.user

		if data.email:
			member.email = data.email
		if data.first_name:
			member.first_name = data.first_name
		if data.last_name:
			member.last_name = data.last_name

		member.save()

		return self.success(member.dictify, meta={'message':'User Updated Successfully.'})

	@normalizer('email')
	def normalize_email(self, email):
		return MemberManager.normalize_email(email)

	@validator('first_name', 'A first name cannot be empty.')
	def validate_first_name_not_empty(cls, first_name):
		return first_name.strip() != ''

	@validator('first_name', 'Invalid characters.')
	def validate_first_name_characters(cls, first_name):
		return True

	@validator('last_name', 'A last name cannot be empty.')
	def validate_last_name_not_empty(cls, last_name):
		return last_name.strip() != ''

	@validator('last_name', 'Invalid characters.')
	def validate_last_name_characters(cls, last_name):
		return True

	@validator('email', 'An account with that email already exists.')
	def validate_email_uniqueness(cls, email):
		new_email = MemberManager.normalize_email(email)
		return not Member.objects.filter(email=new_email).exists()

	@validator('email', 'Not a valid email address.')
	def validate_email_format(cls, email):
		validator = EmailValidator()
		try:
			validator(email)
			return True
		except ValidationError:
			return False


class GetMemberProfile(CommandHandlerBase):

	command_name = 'GET_MEMBER_PROFILE'

	auth_required = True

	def handle(self, data):
		return self.success(self.user.profile.dictify)


class UpdateMemberProfile(CommandHandlerBase):

	command_name = 'UPDATE_MEMBER_PROFILE'

	auth_required = True

	params = [
		Param('phone', Types.STRING, False),
		Param('slogan', Types.STRING, False),
		Param('biography', Types.STRING, False),
		Param('image', Types.FILE, False),
		Param('should_text', Types.STRING, False),
		Param('should_email', Types.STRING, False)
	]

	def handle(self, data):

		profile = self.user.profile

		if data.phone:
			profile.phone = data.phone
		if data.slogan:
			profile.slogan = data.slogan
		if data.biography:
			profile.biography = data.biography
		if data.should_text:
			profile.should_text = data.should_text == 'true'
		if data.should_email:
			profile.should_email = data.should_email == 'true'
		if data.image:
			# TODO: properly determine the extension / validate the image first.
			profile.image = data.image

		profile.save()

		return self.success(profile.dictify, {'message': 'Profile Updated Successfully.'})


class ChangeMemberPassword(CommandHandlerBase):

	command_name = 'CHANGE_MEMBER_PASSWORD'

	auth_required = True

	params = [
		Param('password', Types.STRING),
		Param('password1', Types.STRING),
		Param('password2', Types.STRING)
	]

	def handle(self, data):

		user = self.user

		password_is_correct = user.check_password(data.password)

		if not password_is_correct:
			return self.error('The provided current password was incorrect.')

		if data.password1 == data.password2:
			user.set_password(data.password1)
			user.save()
			self.user = authenticate(username=user.get_username(), password=data.password1)
			login(self.request, self.user)
			return self.success(None, meta={'message': 'The user password was updated successfully.'})
		else:
			return self.error('The provided passwords did not match.')


class ValidateUsername(CommandHandlerBase):

	command_name = 'VALIDATE_EMAIL'

	params = [
		Param('email', Types.STRING)
	]

	@normalizer('email')
	def normalize_email(cls, email):
		return MemberManager.normalize_email(email)

	def handle(self, data):

		exists = Member.objects.filter(email=data.email).exists()

		valid = not exists

		if self.user.is_authenticated():
			if data.email == self.user.email:
				valid = True

		if not valid:
			message = 'An account with this email already exists.'.format(data.email)
		else:
			message = None

		return self.success({'valid': valid, 'message': message})



class ValidatePassword(CommandHandlerBase):

	command_name = 'VALIDATE_PASSWORD'

	auth_required = True

	params = [Param('password', Types.STRING)]

	def handle(self, data):

		password_is_correct = self.user.check_password(data.password)

		if not password_is_correct:
			message = 'Current password is incorrect.'
		else:
			message = None

		return self.success({'valid': password_is_correct, 'message': message})