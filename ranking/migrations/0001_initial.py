# Generated by Django 4.2 on 2024-09-27 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ranking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matches', models.IntegerField(default=0)),
                ('wins', models.IntegerField(default=0)),
                ('loses', models.IntegerField(default=0)),
                ('win_rate', models.FloatField(default=0.0)),
            ],
        ),
    ]
