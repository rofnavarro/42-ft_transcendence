from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from users.models import CustomUser
from match.models import Match

class Ranking(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	matches = models.IntegerField(default=0)
	wins = models.IntegerField(default=0)
	loses = models.IntegerField(default=0)
	win_rate = models.FloatField(default=0.0)

	def __str__(self):
		return str(self.user) if self.user else ''

	def update_win_rate(self):
		if self.matches > 0:
			self.win_rate = (self.wins / self.matches) * 100
		else:
			self.win_rate = 0.0
		self.save()

@receiver(post_save, sender=Match)
def update_ranking_on_match_save(sender, instance, created, **kwargs):
	if created:
		user1_ranking, created = Ranking.objects.get_or_create(user=instance.user1)
		user2_ranking, created = Ranking.objects.get_or_create(user=instance.user2)

		user1_ranking.matches += 1
		user2_ranking.matches += 1

		if instance.winner == instance.user1:
			user1_ranking.wins += 1
			user2_ranking.loses += 1
		elif instance.winner == instance.user2:
			user1_ranking.loses += 1
			user2_ranking.wins += 1

		user1_ranking.update_win_rate()
		user2_ranking.update_win_rate()

@receiver(post_delete, sender=Match)
def update_ranking_on_match_delete(sender, instance, **kwargs):
	user1_ranking = Ranking.objects.get(user=instance.user1)
	user2_ranking = Ranking.objects.get(user=instance.user2)

	user1_ranking.matches -= 1
	user2_ranking.matches -= 1

	if instance.winner == instance.user1:
		user1_ranking.wins -= 1
		user2_ranking.loses -= 1
	elif instance.winner == instance.user2:
		user1_ranking.loses -= 1
		user2_ranking.wins -= 1

	user1_ranking.update_win_rate()
	user2_ranking.update_win_rate()
