from django.shortcuts import render

def	gamepage(request):
	return render(request, 'match/game.html')
