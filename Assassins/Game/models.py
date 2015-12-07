from django.core.urlresolvers import reverse_lazy, reverse
from django.db import models
from Helpers.encryption import *
from .app import GameAppConfig
from itertools import chain
from django.conf import settings

# The parent object that represents an instance of a game
class Game(models.Model):
	title = models.CharField(max_length=255)
	intro = models.TextField(max_length=512)
	location = models.ForeignKey('Site.Location')
	owner = models.ForeignKey(settings.AUTH_USER_MODEL)
	reviewers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='reviewers')
	players = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='players')
	rules = models.ForeignKey('RuleSet', related_name='rules')
	hash = models.CharField(max_length=255, unique=True, null=True, blank=True)
	in_progress = models.BooleanField(default=False)
	open = models.BooleanField(default=True)
	start_date = models.DateTimeField()
	end_date = models.DateTimeField(null=True, blank=True)

	def get_kill_count(self, user):
		return len([assignment for assignment in self.assignments
					if assignment.success and assignment.killer==user])

	def get_is_alive(self, user):
		return any([assignment.success and assignment.killee==user for assignment in self.assignments])

	def get_user_is_owner(self, user):
		return user == self.owner

	def get_user_is_reviewer(self, user):
		return self.reviewers.filter(pk = user.pk).exists()

	def get_user_is_player(self, user):
		return self.players.filter(pk = user.pk).exists()

	def get_user_is_associated(self, user):
		return user in chain(self.reviewers.all(), self.players.all(), [self.owner])

	@property
	def progress(self):
		assignments = self.assignments
		success_count = len([assignment for assignment in assignments if assignment.success])
		return 100 * success_count / len(assignments) if assignments >= 0 else 0

	@property
	def url(self):
		return reverse('games:view', kwargs={'pk':self.pk})

	@property
	def join_url(self):
		return reverse('games:join', kwargs={'hash': self.hash})

	@property
	def associated_users(self):
		return list(chain(self.reviewers.all(), self.players.all(), [self.owner]))

	@property
	def announcements(self):
		return Announcement.objects.filter(game=self).order_by('-date')

	@property
	def assignments(self):
		return Assignment.objects.filter(game=self).order_by('-assigned')


	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

		# if initial save is with a public rule set, then generate a private copy
		if self.rules.public:
			self.rules = self.rules.make_private_copy()

		# save the instance to get a unique id from the database
		super(Game, self).save(force_insert, force_update, using, update_fields)

		#use the unique id to generate the unique hash for the game
		if not self.hash:
			self.hash = encrypt(str(self.pk), settings.SECRET_KEY)
			self.save()


	def __str__(self):
		return self.title


# a set of rules that make up a game
class RuleSet(models.Model):
	public = models.BooleanField(default=True)
	name = models.CharField(max_length=255)
	html = models.TextField(max_length=2048)
	icon_class = models.CharField(max_length=255)

	def make_private_copy(self):
		new = RuleSet(public=False, name=self.name, html=self.html, icon_class=self.icon_class)
		new.save()
		return new

	def __str__(self):
		return "Name: {0} Public: {1}".format(self.name, self.public)


# announcements are notifications that reviewers can send to the entire set of players
class Announcement(models.Model):
	game = models.ForeignKey('Game')
	subject = models.CharField(max_length=255)
	html = models.TextField(max_length=512)
	date = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(settings.AUTH_USER_MODEL)

	def __str__(self):
		return "Announcement about '{0}' for game '{1}'".format(self.subject,str(self.game))



# represents a kill assignment that is either in limbo or completed
class Assignment(models.Model):
	game = models.ForeignKey('Game')
	assigned = models.DateTimeField(auto_now_add=True, auto_created=True)
	closed = models.DateTimeField(blank=True, null=True)
	killer_verdict = models.NullBooleanField(blank=True, null=True)
	killee_verdict = models.NullBooleanField(blank=True, null=True)
	admin_verdict = models.NullBooleanField(blank=True, null=True)
	killer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='killer')
	killee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='killee')
	status = models.CharField(max_length=1, choices=GameAppConfig.STATUSES, default='I')

	@property
	def success(self):
		return self.status == GameAppConfig.SUCCESS

	@property
	def failure(self):
		return self.status == GameAppConfig.FAILED

	@property
	def pending(self):
		return self.status == GameAppConfig.PENDING

	@property
	def incomplete(self):
		return self.status == GameAppConfig.INCOMPLETE

	@property
	def complete(self):
		return self.success or self.failure

	@property
	def needs_admin_review(self):
		return self.admin_verdict is None and self.killee_verdict != self.killer_verdict and \
			   all([x is not None for x in [self.killee_verdict, self.killer_verdict]])

	@property
	def dictify(self):
		killer_dict = self.killer.dictify
		killee_dict = self.killee.dictify

		return {
			'status': self.status,
			'killer': killer_dict,
			'killee': killee_dict,
			'killer_verdict': self.killer_verdict,
			'killee_verdict': self.killee_verdict,
			'admin_verdict': self.admin_verdict
		}


	# method responsible for determining the current state of the assignment
	def set_status_based_on_verdicts(self):
		if not self.complete:

			# admin overrides all
			if self.admin_verdict is not None:
				if self.admin_verdict:
					self.status = GameAppConfig.SUCCESS
				else:
					self.status = GameAppConfig.FAILED

				return

			# if both people have submitted then check that they agree
			if self.killer_verdict is not None and self.killee_verdict is not None:
				if self.killer_verdict and self.killee_verdict:
					self.status = GameAppConfig.SUCCESS
					return

			if any([verdict is not None for verdict in (self.killer_verdict, self.killee_verdict)]):
				self.status = GameAppConfig.PENDING
				return

			self.status = GameAppConfig.INCOMPLETE


	def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
		self.set_status_based_on_verdicts()
		return super(Assignment, self).save(force_insert, force_update, using, update_fields)

	def __str__(self):
		return "Game: {0}, Killer: {1}, Killee: {2}.".format(self.game, self.killer, self.killee)