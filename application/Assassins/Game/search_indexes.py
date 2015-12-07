from .models import *
from haystack import indexes


class GameIndex(indexes.SearchIndex, indexes.Indexable):

	template = 'Game/search/game_text.html'

	text = indexes.CharField(document=True, use_template=True, template_name=template)
	title = indexes.CharField(model_attr='title')

	def index_queryset(self, using=None):
		return Game.objects.all()

	def get_model(self):
		return Game
