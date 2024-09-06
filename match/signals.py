from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Match
from users.models import CustomUser

@receiver(post_save, sender=Match)
def	update_user_stats_on_match_save(sender, instance, created, **kwargs):
	if created:
		update_player_stats(instance.user1)
		update_player_stats(instance.user2)

@receiver(post_delete, sender=Match)
def	update_user_stats_on_match_delete(sender, instance, **kwargs):
	update_player_stats(instance.user1)
	update_player_stats(instance.user2)

def	update_player_stats(user):
	from match.models import Match

	total_matches_played = user.total_matches_played
	total_wins = user.total_wins
	total_loses = user.total_loses
	pass
