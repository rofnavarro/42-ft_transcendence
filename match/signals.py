from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.apps import apps

@receiver(post_save, sender='match.Match')  # Referência em string
def update_user_stats_on_match_save(sender, instance, created, **kwargs):
    if created:
        update_player_stats(instance.user1)
        update_player_stats(instance.user2)

@receiver(post_delete, sender='match.Match')  # Referência em string
def update_user_stats_on_match_delete(sender, instance, **kwargs):
    update_player_stats(instance.user1)
    update_player_stats(instance.user2)

def update_player_stats(user):
    CustomUser = apps.get_model('users', 'CustomUser')  # Importação lazy
    user = CustomUser.objects.get(pk=user.pk)  # Recuperar o usuário do banco de dados

    # Aqui você pode realizar as atualizações
    total_matches_played = user.total_matches_played
    total_wins = user.total_wins
    total_loses = user.total_loses

    # Atualize os atributos de acordo com a lógica do seu jogo
    # Exemplo:
    user.total_matches_played += 1  # Aumenta o total de partidas jogadas
    # Se necessário, adicione lógica para atualizar vitórias ou derrotas
    user.save()  # Salva as mudanças no usuário
