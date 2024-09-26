from django.db import models
from users.models import CustomUser
from django.core.exceptions import ValidationError

class Tournament(models.Model):
    owner = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    players = models.ManyToManyField(CustomUser, related_name='tournaments')

    def str(self):
        return str(self.id)

    def clean(self):
        if self.players.count() < 4 or self.players.count() > 8:
            raise ValidationError('The number of players must be between 4 and 8.')

    def save(self, args, **kwargs):
        self.clean()
        super().save(args, **kwargs)
