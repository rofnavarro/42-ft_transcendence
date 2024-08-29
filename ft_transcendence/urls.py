from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
	path('', views.homepage),
	path('about/', views.aboutpage),
	path('ranking/', include('ranking.urls')),
	path('login/', include('login.urls')),
]
