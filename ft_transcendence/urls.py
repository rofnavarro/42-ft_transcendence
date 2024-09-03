from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.homepage, name='home'),
	path('error/', views.errorpage, name='error'),
    path('admin/', admin.site.urls),
	path('about/', views.aboutpage),
	path('game/', views.gamepage),
	path('ranking/', include('ranking.urls')),
	path('login/', include('login.urls')),
	path('users/', include('users.urls')),
]
