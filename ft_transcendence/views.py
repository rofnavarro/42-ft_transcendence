from django.shortcuts import render
from django.utils import translation
from django.shortcuts import redirect

def	homepage(request):
	return render(request, 'home.html')

def	aboutpage(request):
	return render(request, 'about.html')

def	errorpage(request):
	return render(request, '404.html')

def set_language(request, language):
	translation.activate(language)
	request.session[translation.LANGUAGE_SESSION_KEY] = language
	return redirect('home')