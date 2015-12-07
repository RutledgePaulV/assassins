from allauth.socialaccount.forms import SignupForm
from django.contrib.auth.admin import UserAdmin

from django.contrib.auth.forms import ReadOnlyPasswordHashField

from django import forms
from django.utils.safestring import mark_safe

from Helpers.services import ImageService
from .models import *


class MemberCreationForm(forms.ModelForm):
	password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
	password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

	class Meta:
		model = Member
		fields = ('email', 'first_name', 'last_name')

	def clean_password2(self):
		password1 = self.cleaned_data.get('password1')
		password2 = self.cleaned_data.get('password2')
		if password1 and password2 and password1 != password2:
			raise forms.ValidationError("Passwords don't match.")
		return password2

	def save(self, commit=True):
		user = super(MemberCreationForm, self).save(commit=False)

		user.set_password(self.cleaned_data['password1'])
		if commit:
			user.save()

			image = ImageService.gravatar_image(user.email)

			if image:
				user.profile.image = image
				user.profile.save()

		return user


class MemberChangeForm(forms.ModelForm):
	password = ReadOnlyPasswordHashField()

	class Meta:
		model = Member
		fields = ('email', 'first_name', 'last_name', 'profile')

	def clean_password(self):
		return self.initial['password']


class MemberAdminForm(UserAdmin):
	form = MemberChangeForm
	add_form = MemberCreationForm

	list_display = ('email', 'first_name', 'last_name', 'is_admin')
	list_filter = ('is_admin',)

	fieldsets = (
		('Account', {'fields': ('email', 'password')}),
		('Info', {'fields': ('first_name', 'last_name')}),
		('Permissions', {'fields': ('is_admin',)})
	)

	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'first_name', 'last_name', 'password1', 'password2')}
		 ),
	)

	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()


class SocialSignupForm(SignupForm):
	def raise_duplicate_email_error(self):
		link = reverse('account_login')
		next = reverse('socialaccount_signup')
		message = "Looks like you already have an account. Sign in first then link them!"
		raise forms.ValidationError(mark_safe("<a href='{0}?next={1}'>{2}</a>".format(link, next, message)))
