from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import BaseUserManager

class	CustomUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, **extra_fields):
		if not email:
			raise ValueError(gettext_lazy('The Email field must be set'))
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, **extra_fields)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError(gettext_lazy('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(gettext_lazy('Superuser must have is_superuser=True.'))

		return self.create_user(email, username, password, **extra_fields)

class	CustomUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(gettext_lazy('email address'), unique=True)
	username = models.CharField(max_length=50, unique=True)
	first_name = models.CharField(gettext_lazy('first name'), max_length=30, blank=True)
	last_name = models.CharField(gettext_lazy('last name'), max_length=30, blank=True)
	date_joined = models.DateTimeField(gettext_lazy('date joined'), default=timezone.now)
	is_active = models.BooleanField(gettext_lazy('active'), default=True)
	is_staff = models.BooleanField(gettext_lazy('staff status'), default=False)
	is_superuser = models.BooleanField(gettext_lazy('superuser status'), default=False)

	objects = CustomUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	class	Meta:
		verbose_name = gettext_lazy('user')
		verbose_name_plural = gettext_lazy('users')

	def __str__(self):
		return self.email
