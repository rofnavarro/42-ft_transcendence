# Generated by Django 4.2 on 2024-09-06 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('match', '0002_remove_match_match_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='user1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_user1', to=settings.AUTH_USER_MODEL, unique=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='user2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matches_as_user2', to=settings.AUTH_USER_MODEL, unique=True),
        ),
    ]