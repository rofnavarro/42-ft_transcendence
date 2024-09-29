from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import set_language

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
	path('tournaments/', include('tournaments.urls')),
	path('set_language/', set_language, name='set_language'),
]



urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)