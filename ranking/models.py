from django.db import models
from users.models import CustomUser

class	Ranking(models.Model):
	user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
	matches = models.IntegerField()
	wins = models.IntegerField()
	loses = models.IntegerField()
	win_rate = models.FloatField()

	def __str__(self):
		return self.user if self.user else ''