from django.contrib import admin
from .models import Tournament, inviteLobby

class TournamentAdmin(admin.ModelAdmin):
	list_display = ('name', 'start_date', 'end_date', 'token')
	list_filter = ('start_date', 'end_date')
	ordering = ['start_date']
	filter_horizontal = ['players']


# Register your models here.
admin.site.register(Tournament, TournamentAdmin)

