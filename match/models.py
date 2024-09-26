from django.core.exceptions import ValidationError
from django.db import models
from users.models import CustomUser
from django.utils.translation import gettext_lazy
from django.utils import timezone

class	Match(models.Model):
	user1 = models.ForeignKey(CustomUser, related_name='matches_as_user1', on_delete=models.CASCADE)
	user2 = models.ForeignKey(CustomUser, related_name='matches_as_user2', on_delete=models.CASCADE)

	date = models.DateTimeField(gettext_lazy('date'), auto_now_add=True)

	score_user1 = models.IntegerField(gettext_lazy('score player 1'), default=0)
	score_user2 = models.IntegerField(gettext_lazy('score player 2'), default=0)

	is_tournament = models.BooleanField(default=False)

	@property
	def	winner(self):
		if self.score_user1 > self.score_user2:
			return self.user1
		elif self.score_user2 > self.score_user1:
			return self.user2
		return None

	@property
	def tournament_hash(self):
		if self.is_tournament:
			return self.hash
			

	def	clean(self):
		if self.user1 == self.user2:
			raise ValidationError("Jogador 1 e jogador 2 precisam ser usuários diferentes.")

	def	save(self, *args, **kwargs):
		self.clean()
		super().save(*args, **kwargs)

	class	Meta:
		constraints = [
			models.UniqueConstraint(fields=['user1', 'user2', 'date'], name='unique_match'),
		]
