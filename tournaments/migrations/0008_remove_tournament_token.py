# Generated by Django 4.2 on 2024-09-13 18:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0007_alter_tournament_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tournament',
            name='token',
        ),
    ]
