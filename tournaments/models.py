from django.db import models
from users.models import CustomUser
from match.models import Match
from django.utils.translation import gettext_lazy
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class	Tournament(models.Model):
	owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	players = models.ManyToManyField(CustomUser, related_name='tournaments')

	date = models.DateTimeField('date', auto_now_add=True)
	is_complete = models.BooleanField(default=False)
	num_players = models.PositiveSmallIntegerField(choices=[(4, '4 Players'), (8, '8 Players')])  # Define o tamanho do torneio
		
	matches = models.ManyToManyField(Match, related_name='tournaments')

	def __str__(self):
		return _(f"Tournament %(self.id)s - %(self.num_players)s players") % {'self.id': self.id, 'self.num_players': self.num_players}

	def save(self, *args, **kwargs):
		if self.players.count() != self.num_players:
			raise ValidationError(_('The number of players must match the tournament type.'))

		required_matches = 3 if self.num_players == 4 else 7
		if self.matches.count() != required_matches:
			raise ValidationError(_('All matches must be completed before saving the tournament.'))
		
		if self.matches.count() == required_matches:
			self.is_complete = True

		super(Tournament, self).save(*args, **kwargs)

	
	# def create_bracket(self):
	# 	"""
	# 	Gera as partidas iniciais para o torneio.
	# 	"""
	# 	players = list(self.players.all())
	# 	if len(players) not in [4, 8]:
	# 		raise ValidationError('The number of players must be 4 or 8 to create a bracket.')
	# 	matches = []
	# 	if len(players) == 4:
	# 		matches.append(Match.objects.create(user1=players[0], user2=players[1], is_tournament=True, tournament=self))
	# 		matches.append(Match.objects.create(user1=players[2], user2=players[3], is_tournament=True, tournament=self))
	# 	elif len(players) == 8:
	# 		matches.append(Match.objects.create(user1=players[0], user2=players[1], is_tournament=True, tournament=self))
	# 		matches.append(Match.objects.create(user1=players[2], user2=players[3], is_tournament=True, tournament=self))
	# 		matches.append(Match.objects.create(user1=players[4], user2=players[5], is_tournament=True, tournament=self))
	# 		matches.append(Match.objects.create(user1=players[6], user2=players[7], is_tournament=True, tournament=self))
	# 	return
	
	# def advance_to_next_round(self):
	# 	"""
	# 	Gera as próximas partidas com os vencedores da rodada anterior.
	# 	"""
	# 	previous_round_matches = Match.objects.filter(tournament=self, winner__isnull=False)
	# 	winners = [match.winner for match in previous_round_matches]

	# 	if len(winners) == 2:
	# 		Match.objects.create(user1=winners[0], user2=winners[1], is_tournament=True, tournament=self)
	# 	elif len(winners) == 4:
	# 		Match.objects.create(user1=winners[0], user2=winners[1], is_tournament=True, tournament=self)
	# 		Match.objects.create(user1=winners[2], user2=winners[3], is_tournament=True, tournament=self)
	# 	return