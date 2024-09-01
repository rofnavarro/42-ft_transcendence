from django.urls import path
from . import views  # Importa as views do app login

app_name = 'login'

urlpatterns = [
	path('', views.login_user, name="login"),  # Ajustado para remover 'login/' repetido
	path('callback/', views.callback, name="callback"),
	path('logout/', views.logout_user, name="logout_user"),
]
