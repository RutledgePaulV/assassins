from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.socialaccount.models import SocialAccount
from Helpers.services import ImageService

class MemberAccountAdapter(DefaultAccountAdapter):

	pass


class MemberSocialAccountAdapter(DefaultSocialAccountAdapter):

	def save_user(self, request, sociallogin, form=None):
		user = super(MemberSocialAccountAdapter, self).save_user(request, sociallogin, form)

		fb_account = SocialAccount.objects.filter(user_id=user.id, provider='facebook')

		if fb_account.exists():
			uid = fb_account[0].uid
			image = ImageService.facebook_image(uid)

			if image:
				user.profile.image = image
				user.profile.save()

		return user
