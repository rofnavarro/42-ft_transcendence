# Generated by Django 4.2 on 2024-09-09 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='nickname',
            field=models.CharField(blank=True, default=models.CharField(max_length=50, unique=True), max_length=50, null=True, unique=True),
        ),
    ]
