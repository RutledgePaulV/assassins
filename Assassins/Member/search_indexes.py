from .models import *
from haystack import indexes


class MemberIndex(indexes.SearchIndex, indexes.Indexable):

	template = 'Member/search/member_text.html'

	text = indexes.CharField(document=True, use_template=True, template_name=template)

	def index_queryset(self, using=None):
		return Member.objects.all()

	def get_model(self):
		return Member
