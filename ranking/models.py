from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import CustomUser
from match.models import Match

class	Ranking(models.Model):
	user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
	matches = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	loses = models.IntegerField(default=0)
	win_rate = models.FloatField(default=0.0)

	@property
	def	formatted_win_rate(self):
		if self.matches > 0:
			win_rate = (self.wins / self.matches) * 100
			return f"{win_rate:.2f}%"
		return "N/A"

	def	update_ranking(self):
		self.matches = self.user.total_matches_played
		self.wins = self.user.total_wins
		self.loses = self.user.total_loses
		self.win_rate = self.wins / self.matches * 100 if self.matches > 0 else 0.0
		self.save()

@receiver(post_save, sender=Match)
@receiver(post_delete, sender=Match)
def	update_ranking(sender, instance, **kwargs):
	try:
		for user in [instance.user1, instance.user2]:
			ranking = Ranking.objects.get(user=user)
			ranking.update_ranking()
	except Ranking.DoesNotExist:
		pass