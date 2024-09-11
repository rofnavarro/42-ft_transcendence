from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
	path('profile/<str:username>/', views.user_profile, name='profile'),
	path('add-friend/<str:username>/', views.send_friend_request, name='send_friend_request'),
	path('friends/', views.view_friends, name='view_friends'),
	path('play/<str:username>/', views.wanna_play, name='wanna_play'),
	path('play/local/<str:username>/', views.local_play, name='local_play'),
]
