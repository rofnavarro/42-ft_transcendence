from django.shortcuts import render
from django.utils import translation
from django.shortcuts import redirect

def	homepage(request):
	return render(request, 'home.html')

def	aboutpage(request):
	return render(request, 'about.html')

def	errorpage(request):
	return render(request, '404.html')

