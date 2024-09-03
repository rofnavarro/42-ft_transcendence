from django.shortcuts import render

def	homepage(request):
	return render(request, 'home.html')

def	aboutpage(request):
	return render(request, 'about.html')

def	errorpage(request):
	return render(request, '404.html')

# DEFINIR A CHAMADA DO JOGO PELO APP MATCHES
def	gamepage(request):
	return render(request, 'game.html')
