from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from users.models import CustomUser

class	Match(models.Model):
	user1 = models.ForeignKey(CustomUser, related_name='matches_as_user1', on_delete=models.CASCADE)
	user2 = models.ForeignKey(CustomUser, related_name='matches_as_user2', on_delete=models.CASCADE)

	date = models.DateTimeField('date', auto_now_add=True)

	score_user1 = models.IntegerField('score player 1', default=0)
	score_user2 = models.IntegerField('score player 2', default=0)

	is_tournament = models.BooleanField(default=False)

	@property
	def	winner(self):
		if self.score_user1 > self.score_user2:
			return self.user1
		elif self.score_user2 > self.score_user1:
			return self.user2
		return None

	def	clean(self):
		if self.user1 == self.user2:
			raise ValidationError(_("Player 1 and Player 2 must be different users."))

	def	save(self, *args, **kwargs):
		self.clean()
		super().save(*args, **kwargs)

	class	Meta:
		constraints = [
			models.UniqueConstraint(fields=['user1', 'user2', 'date'], name='unique_match'),
		]
