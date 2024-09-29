from django.urls import path
from . import views

app_name = 'match'

urlpatterns = [
	path('', views.gamepage, name="match"),
	path('tournament_games', views.tournament_games, name="tournament_games"),
	path('tournament_final', views.tournament_final, name="tournament_final"),
	path('history/<str:username>/', views.history, name="history"),
	path('save_match_ajax', views.save_match_ajax, name="save_match_ajax"),
	path('save_match_ajax_4', views.save_match_ajax_4, name="save_match_ajax_4"),
]
