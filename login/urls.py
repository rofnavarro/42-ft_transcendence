from django.urls import path
from ft_transcendence.views import homepage
from . import views

app_name = 'login'

urlpatterns = [
	path('', homepage, name="login"),
	path('manual_login/', views.manual_login, name="manual_login"),
	path('callback/', views.callback, name="callback"),
	path('logout/', views.logout_user, name="logout_user"),
	path('set_email/', views.set_email, name='set_email'),
	path('set_password/', views.set_password, name='set_password'),
	path('2fa/', views.verify_2fa_code_email, name='verify2fa'),
]
