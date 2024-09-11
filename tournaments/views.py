from django.shortcuts import render
from .models import Tournament

# Create your views here.

def tournament(request):
	tournament = Tournament.objects.all().order_by('-start_date')
	# TODO: web3 fica aqui para pegar da blockchain e montar o objeto que vai para o front
	# talvez o mesmo fluxo funcione para o fim do torneio que ira cadastrar na blockchain um novo torneio
	# objectToFront = web.gettournament(tournament[1]
	return render(request, 'tournaments/tournaments.html', {'tournament': tournament})