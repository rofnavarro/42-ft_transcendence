# Generated by Django 4.2 on 2024-09-05 05:06

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='profile_picture',
            field=models.ImageField(blank=True, default="{% static 'imgs/banana.png' %}", null=True, upload_to=users.models.user_profile_picture_path),
        ),
    ]
