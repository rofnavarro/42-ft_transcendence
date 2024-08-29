from django.db import models

class	Ranking(models.Model):
	user = models.SlugField(max_length=20)
	matches = models.IntegerField()
	wins = models.IntegerField()
	loses = models.IntegerField()
	win_rate = models.FloatField()

	def __str__(self):
		return self.user if self.user else ''