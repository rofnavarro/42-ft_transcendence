from django.shortcuts import render
from .models import Ranking

def	ranking_list(request):
	ranking = Ranking.objects.all().order_by('-win_rate')
	return render(request, 'ranking/ranking.html', { 'ranking': ranking })