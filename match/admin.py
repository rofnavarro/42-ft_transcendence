# admin.py
from django.contrib import admin
from .models import Match

class	MatchAdmin(admin.ModelAdmin):
	list_display = ('user1', 'user2', 'date', 'score_user1', 'score_user2', 'is_tournament', 'winner')
	list_filter = ('is_tournament', 'date')
	search_fields = ('user1__username', 'user2__username')
	ordering = ('-date',)

	def winner(self, obj):
		return obj.winner.username if obj.winner else "Empate"

	winner.short_description = 'Winner'

admin.site.register(Match, MatchAdmin)
