# Generated by Django 4.2 on 2024-09-04 23:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_is_online_customuser_last_online_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]