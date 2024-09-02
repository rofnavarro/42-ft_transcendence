from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
	path('', views.login_user, name="login"),
	path('callback/', views.callback, name="callback"),
	path('logout/', views.logout_user, name="logout_user"),
]
