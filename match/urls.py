from django.urls import path
from . import views

app_name = 'match'

urlpatterns = [
	path('', views.gamepage, name="match"),
	path('history/', views.history, name="history"),
	path('save_match_ajax', views.save_match_ajax, name="save_match_ajax"),
	path('save_match_ajax_4', views.save_match_ajax_4, name="save_match_ajax_4"),
]
