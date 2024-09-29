from django.db import models
from users.models import CustomUser
from match.models import Match
from django.utils.translation import gettext_lazy as _

class	Tournament(models.Model):
	owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE, related_name='owned_tournaments')
	date = models.DateTimeField('date', auto_now_add=True)
	matches = models.ManyToManyField(Match, related_name='tournaments')
	winner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE,  related_name='won_tournaments')

	def __str__(self):
		return f"{_('Tournament')} {self.id}"

	def save(self, *args, **kwargs):
		super(Tournament, self).save(*args, **kwargs)