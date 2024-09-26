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
		
		usernames = [
			request.POST.get('player1-nickname'),
			request.POST.get('player2-nickname'),
			request.POST.get('player3-nickname'),
			request.POST.get('player4-nickname'),
		]
		usernames = [username for username in usernames if username]

		turns = request.POST.get('qtd-turnos')

		return render(request, 'match/game.html', {'players': players, 'usernames': usernames, 'turns': turns})
	return render(request, 'home')
