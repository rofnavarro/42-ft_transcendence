from django.db import models
from django.contrib import admin
from users.models import CustomUser
import random

# Create your models here.

class Tournament(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	# TODO: trocar o DateField para DateTimeField pois assim podemos ter mais controle do tempo
	start_date = models.DateField()
	end_date = models.DateField()
	players = models.ManyToManyField('self', symmetrical=True, through='inviteLobby')
	token = random.randint(100000, 999999)

	def __str__(self):
		return self.name



class inviteLobby(models.Model):
	user1 = models.ForeignKey(CustomUser, related_name='owner', on_delete=models.CASCADE)
	user2 = models.ForeignKey(CustomUser, related_name='inviter',on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user1', 'user2')
