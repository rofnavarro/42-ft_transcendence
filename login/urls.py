from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
	path('', views.login_user, name="login"),
	path('manual_login/', views.manual_login, name="manual_login"),
	path('callback/', views.callback, name="callback"),
	path('logout/', views.logout_user, name="logout_user"),
	path('set_password/', views.set_password, name='set_password')
]
