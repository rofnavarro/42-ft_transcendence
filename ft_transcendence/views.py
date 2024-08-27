# from django.http import HttpResponse
from django.shortcuts import render

def	homepage(request):
	# return HttpResponse("Transcendencenana")
	return render(request, 'home.html')

def	aboutpage(request):
	# return HttpResponse("Banana Team")
	return render(request, 'about.html')
