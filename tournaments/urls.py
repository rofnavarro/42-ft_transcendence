from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
	path('', views.tournament, name='tournaments'),
	path('tournament_4/', views.tournament_4, name='tournament_4'),
	path('tournament_8/', views.tournament_8, name='tournament_8'),
]
	
