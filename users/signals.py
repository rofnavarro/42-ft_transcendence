from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import CustomUser
from ranking.models import Ranking

@receiver(post_save, sender=CustomUser)
def create_or_update_ranking(sender, instance, created, **kwargs):
	if created:
		Ranking.objects.create(user=instance)
