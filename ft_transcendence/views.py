from django.shortcuts import render

def	homepage(request):
	return render(request, 'home.html')

def	aboutpage(request):
	return render(request, 'about.html')
