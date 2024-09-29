from django.contrib import admin
from .models import Tournament

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'display_matches')
    
    def display_matches(self, obj):
        return ", ".join(str(match) for match in obj.matches.all())

    display_matches.short_description = 'Matches'
admin.site.register(Tournament, TournamentAdmin)