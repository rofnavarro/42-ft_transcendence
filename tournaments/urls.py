from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
	path('', views.tournaments, name='tournaments'),
	path('tournament_4/', views.tournament_4, name='tournament_4'),
]
	
