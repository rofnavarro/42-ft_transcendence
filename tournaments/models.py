from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy
from users.models import CustomUser
import random

# Create your models here.
class Tournament(models.Model):
	name = models.CharField(max_length=50)
	owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
	start_date = models.DateTimeField(gettext_lazy('start'), default=timezone.now)
	end_date = models.DateTimeField(gettext_lazy('end'), default=timezone.now)
	players = models.ManyToManyField('self', symmetrical=True, through='inviteLobby')
	# TODO: usar timestamp para criar o token
	token = random.randint(100000, 999999)

	def __str__(self):
		return self.name


class inviteLobby(models.Model):
	user1 = models.ForeignKey(CustomUser, related_name='owner', on_delete=models.CASCADE)
	user2 = models.ForeignKey(CustomUser, related_name='inviter',on_delete=models.CASCADE)

	class Meta:
		unique_together = ('user1', 'user2')
