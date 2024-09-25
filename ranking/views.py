from django.shortcuts import render
from .models import Ranking
from django.http import HttpRequest

def	ranking(request):
	# token = request.COOKIES.get('nana_token')
	response = HttpRequest()

	token = response.get_signed_cookie('nana_token')
	print("Meu token", token)

	ranking = Ranking.objects.all().order_by('-win_rate')
	return render(request, 'ranking/ranking.html', { 'ranking': ranking })