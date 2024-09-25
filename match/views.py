from django.shortcuts import render

def	gamepage(request):
	if request.method == 'POST':
		players = [
			request.POST.get('player1'),
			request.POST.get('player2'),
			request.POST.get('player3'),
			request.POST.get('player4'),
		]

		turns = request.POST.get('qtd-turnos')
		players = [player for player in players if player]
		return render(request, 'match/game.html', {'players': players, 'turns': turns})
	return render(request, 'match/game.html')
