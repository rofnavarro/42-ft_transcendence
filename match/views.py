from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db.models import Q
from users.models import CustomUser
from tournaments.models import Tournament
from tournaments.views import set_tournament
from .models import Match
import json
from django.db import transaction


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
		usernames = [
			request.POST.get('player1'),
			request.POST.get('player2'),
			request.POST.get('player3'),
			request.POST.get('player4'),
		]
		usernames = [username for username in usernames if username]
		
		nicknames = [
			request.POST.get('player1-nickname'),
			request.POST.get('player2-nickname'),
			request.POST.get('player3-nickname'),
			request.POST.get('player4-nickname'),
		]
		nicknames = [nickname for nickname in nicknames if nickname]

		turns = request.POST.get('qtd-turnos')

		color = request.POST.get('background')
		return render(request, 'match/game.html', {'usernames': usernames, 'nicknames': nicknames, 'turns': turns, 'color': color})
	return render(request, 'home.html')


def tournament_games(request):
	if request.method == 'POST':
		usernames = [
			request.POST.get('player1'),
			request.POST.get('player2'),
			request.POST.get('player3'),
			request.POST.get('player4'),
		]		
		nicknames = [
			request.POST.get('player1-nickname'),
			request.POST.get('player2-nickname'),
			request.POST.get('player3-nickname'),
			request.POST.get('player4-nickname'),
		]
		turns = request.POST.get('turns')
		return render(request, 'match/tournament_games.html', {'usernames': usernames, 'nicknames': nicknames, 'turns': turns})
	return render(request, 'tournaments:tournament_4')

def tournament_final(request):
	if request.method == 'POST':
		user1 = request.POST.get('match-resultA-player')
		user1 = CustomUser.objects.get(username=user1)
		
		user2 =	request.POST.get('match-resultB-player')
		user2 = CustomUser.objects.get(username=user2)
		
		score_user1 = int(request.POST.get('match-resultA-score'))
		score_user2 = int(request.POST.get('match-resultB-score'))

		match1 = Match.objects.create(user1=user1, user2=user2, score_user1=score_user1, score_user2=score_user2, is_tournament=True)

		user3 =	request.POST.get('match-resultC-player')
		user3 = CustomUser.objects.get(username=user3)
		
		user4 =	request.POST.get('match-resultD-player')
		user4 = CustomUser.objects.get(username=user4)

		score_user3 = int(request.POST.get('match-resultC-score'))
		score_user4 = int(request.POST.get('match-resultD-score'))

		match2 = Match.objects.create(user1=user3, user2=user4, score_user1=score_user3, score_user2=score_user4, is_tournament=True)
		
		winner1 = request.POST.getlist('winner1')
		winner1 = [winner for winner in winner1 if winner]
		winner2 = request.POST.getlist('winner2')
		winner2 = [winner for winner in winner2 if winner]


		winner1_nickname = winner1[0]
		winner1 = CustomUser.objects.get(nickname=winner1_nickname)

		winner2_nickname = winner2[0]
		winner2 = CustomUser.objects.get(nickname=winner2_nickname)

		owner = CustomUser.objects.get(username=user1)

		turns = int(request.POST.get('turns'))

		t = None
		try:
			with transaction.atomic():
				tournament = Tournament.objects.create(owner=owner)
				tournament.matches.add(match1, match2)
				tournament.save()
				t = tournament

		except Exception as e:
			return render(request, 'home.html')

		return render(request, 'match/tournament_final.html', {'id_tournament': t, 'turns': turns, 'user1': winner1, 'user2': winner2})
	user = get_object_or_404(CustomUser, username=user1)
	return render(request, 'users/wanna_play.html', {'user': user})

def finish_tournament(request):
	username = request.user
	user = get_object_or_404(CustomUser, username=username)
	if request.method == 'POST':
		user1 = request.POST.get('match-resultA-player')
		user1 = CustomUser.objects.get(username=user1)
		
		user2 =	request.POST.get('match-resultB-player')
		user2 = CustomUser.objects.get(username=user2)
		
		score_user1 = int(request.POST.get('match-resultA-score'))
		score_user2 = int(request.POST.get('match-resultB-score'))

		match1 = Match.objects.create(user1=user1, user2=user2, score_user1=score_user1, score_user2=score_user2, is_tournament=True)

		t = request.POST.get('tournament')
		try:
			with transaction.atomic():
				tournament = Tournament.objects.get(id=t)
				tournament.matches.add(match1)
				if (score_user1 > score_user2):
					tournament.winner = user1
				elif (score_user1 < score_user2):
					tournament.winner = user2
				tournament.save()
				set_tournament(tournament.id)
		except Exception as e:
			print(e)
			return render(request, 'home.html')
		return render(request, 'users/wanna_play.html', {'user': user})
	return render(request, 'users/wanna_play.html', {'user': user})

@login_required
def history(request, username):
	user = get_object_or_404(CustomUser, username=username)
	matches = Match.objects.filter(Q(user1=user) | Q(user2=user)).order_by('-date')
	return render(request, 'match/history.html', {'user': user, 'matches': matches})