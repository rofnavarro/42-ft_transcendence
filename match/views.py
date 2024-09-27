from django.shortcuts import render
from .models import Match
from django.http import JsonResponse
import json
from users.models import CustomUser

def save_match_ajax(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			user1 = data.get('user1')
			user2 = data.get('user2')
			score_user1 = data.get('score_user1')
			score_user2 = data.get('score_user2')

			usera = CustomUser.objects.get(username=user1)
			userb = CustomUser.objects.get(username=user2)

			match = Match.objects.create(
				user1=usera,
				user2=userb,
				score_user1=score_user1,
				score_user2=score_user2
			)
			match.save()

			return JsonResponse({'status': 'success', 'match_id': match.id})
		except Exception as e:
			return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


def save_match_ajax_4(request):
	if request.method == 'POST':
		try:
			data = json.loads(request.body)
			user1 = data.get('user1')
			user2 = data.get('user2')
			user3 = data.get('user3')
			user4 = data.get('user4')
			score_user1 = data.get('score_user1')
			score_user2 = data.get('score_user2')
			score_user3 = data.get('score_user3')
			score_user4 = data.get('score_user4')

			usera = CustomUser.objects.get(username=user1)
			userb = CustomUser.objects.get(username=user2)
			userc = CustomUser.objects.get(username=user3)
			userd = CustomUser.objects.get(username=user4)

			match1 = Match.objects.create(
				user1=usera,
				user2=userb,
				score_user1=score_user1,
				score_user2=score_user2
			)
			match1.save()

			match2 = Match.objects.create(
				user1=usera,
				user2=userd,
				score_user1=score_user1,
				score_user2=score_user4
			)
			match2.save()

			match3 = Match.objects.create(
				user1=userc,
				user2=userb,
				score_user1=score_user3,
				score_user2=score_user2
			)
			match3.save()

			match4 = Match.objects.create(
				user1=userc,
				user2=userd,
				score_user1=score_user3,
				score_user2=score_user4
			)
			match4.save()
			return JsonResponse({'status': 'success'})
		except Exception as e:
			return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
	else:
		return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)


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

		color = request.POST.get('background')

		return render(request, 'match/game.html', {'players': players, 'usernames': usernames, 'turns': turns, 'color': color})
	return render(request, 'home.html')
