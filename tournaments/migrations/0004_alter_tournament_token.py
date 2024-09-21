# Generated by Django 4.2 on 2024-09-12 21:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_tournament_token_alter_tournament_end_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tournament',
            name='token',
            field=models.CharField(default=uuid.uuid4, max_length=6, unique=True),
        ),
    ]