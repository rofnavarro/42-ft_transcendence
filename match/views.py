from django.shortcuts import render

def	gamepage(request):
	if request.method == 'POST':
		players = [
			request.POST.get('player1'),
			request.POST.get('player2'),
			request.POST.get('player3'),
			request.POST.get('player4'),
		]
		players = [player for player in players if player]
		return render(request, 'match/game.html', {'players': players})
	return render(request, 'match/game.html')
