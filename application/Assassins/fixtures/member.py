from Member.models import Member
from .default import BaseFixture


class MemberFixture(BaseFixture):

	def run(self, index):

		email = self.random_email()

		while True:
			if not Member.objects.filter(email=email).exists():
				break
			else:
				email = self.random_email()

		first_name = email.split('.')[0]
		last_name = email.split('.')[1].split('@')[0]

		user = Member(
			email=email,
			first_name=first_name,
			last_name=last_name
		)

		user.set_password('test')
		user.save()

		user.profile.phone = self.random_phone()
		user.profile.image = self.random_image(width=400, height=400)
		user.profile.slogan = self.random_block(10)
		user.profile.biography = self.random_block(40)
		user.profile.should_email = self.random_boolean()
		user.profile.should_text = self.random_boolean()

		user.profile.save()