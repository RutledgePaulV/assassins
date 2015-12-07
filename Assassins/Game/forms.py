from django import forms
from django.forms import ModelForm, Form
from Game.models import Game, RuleSet
from Site.app import SiteAppConfig


class GameCreationForm(Form):

	title = forms.CharField(max_length=255, required=True)
	cover = forms.ImageField(required=True)
	rules = forms.ModelChoiceField(queryset=RuleSet.objects.filter(public=True), widget=forms.HiddenInput())
	intro_widget = forms.Textarea(attrs={'cols': 80, 'rows': 5})
	intro = forms.CharField(max_length=512, widget=intro_widget, required=True)
	address = forms.CharField(max_length=255, required=True)
	state = forms.ChoiceField(choices=SiteAppConfig.STATES, required=True)
	city = forms.CharField(max_length=255, required=True)
	zip = forms.CharField(max_length=5, required=True)