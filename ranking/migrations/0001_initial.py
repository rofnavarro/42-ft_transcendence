# Generated by Django 4.2 on 2024-08-28 20:24

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
                ('user', models.CharField(max_length=20)),
                ('matches', models.IntegerField()),
                ('wins', models.IntegerField()),
                ('loses', models.IntegerField()),
                ('win_rate', models.FloatField()),
            ],
        ),
    ]