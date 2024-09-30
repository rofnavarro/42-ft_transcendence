from django.apps import apps
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender='users.CustomUser')  # Usar a string para evitar problemas de importação
def create_or_update_ranking(sender, instance, created, **kwargs):
    if created:
        Ranking = apps.get_model('ranking', 'Ranking')  # Obtenha o modelo de forma preguiçosa
        Ranking.objects.create(user=instance)
