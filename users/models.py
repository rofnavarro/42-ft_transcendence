from django.db import models

class	User(models.Model):
	username = models.SlugField(max_length=20)
