from django.shortcuts import render
from .models import Ranking
from django.http import HttpRequest

def	ranking(request):
	ranking = Ranking.objects.all().order_by('-win_rate')
	return render(request, 'ranking/ranking.html', { 'ranking': ranking })