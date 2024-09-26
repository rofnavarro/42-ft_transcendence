from django.contrib import admin
from .models import Tournament

class TournamentAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'get_players')
    filter_horizontal = ('players',)

    def get_players(self, obj):
        return ", ".join([player.username for player in obj.players.all()])
    get_players.short_description = 'Players'

admin.site.register(Tournament, TournamentAdmin)