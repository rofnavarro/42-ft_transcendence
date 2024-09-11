from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
	path('', views.homepage, name='home'),
	path('error/', views.errorpage, name='error'),
    path('admin/', admin.site.urls),
	path('about/', views.aboutpage),
	path('match/', include('match.urls')),
	path('ranking/', include('ranking.urls')),
	path('login/', include('login.urls')),
	path('users/', include('users.urls')),
	path('tournament/', include('tournaments.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)