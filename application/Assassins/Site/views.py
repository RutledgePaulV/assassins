from django.shortcuts import render


def index(request):
	return render(request, 'Site/index.html', {})


def geek(request):
	return render(request, 'Site/geek.html', {})


def thanks(request):
	return render(request, 'Site/thanks.html', {})


def contact(request):
	return render(request, 'Site/contact.html', {})
