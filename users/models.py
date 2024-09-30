from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

import os

def	user_profile_picture_path(instance, filename):
	_, ext = os.path.splitext(filename)
	return f'profile_pictures/{slugify(instance.username)}_profile_picture{ext}'

class	CustomUserManager(BaseUserManager):
	def	create_user(self, email, username, password=None, **extra_fields):
		if not username:
			raise ValueError(_('A username is needed.'))
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, nickname=username, **extra_fields)
		user.set_unusable_password()
		user.save(using=self._db)
		return user

	def	create_superuser(self, email, username, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)
		if extra_fields.get('is_staff') is not True:
			raise ValueError(_('Superuser must have is_staff=True.'))
		if extra_fields.get('is_superuser') is not True:
			raise ValueError(_('Superuser must have is_superuser=True.'))
		return self.create_user(email, username, password, **extra_fields)

class	CustomUser(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=20, unique=True)
	nickname = models.CharField(max_length=20,unique=True, null=True, blank=True, default=username)
	email = models.EmailField('email address', unique=True)

	token = models.CharField(max_length=300, blank=True, null=True)

	first_name = models.CharField('first name', max_length=30, blank=True)
	last_name = models.CharField('last name', max_length=30, blank=True)
	profile_picture = models.ImageField(upload_to=user_profile_picture_path, blank=True, null=True)

	verification_code = models.IntegerField('2fa_code', blank=True, null=True)
	is_verified = models.BooleanField('verified status', default=False)

	date_joined = models.DateTimeField('date joined', default=timezone.now)
	is_active = models.BooleanField('active', default=True)
	
	is_staff = models.BooleanField('staff status', default=False)
	is_superuser = models.BooleanField('superuser status', default=False)

	is_online = models.BooleanField(default=False)
	last_online = models.DateTimeField(default=timezone.now)
	
	friends = models.ManyToManyField('self', symmetrical=False, through='Friendship')

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []


	class	Meta:
		verbose_name = ('user')
		verbose_name_plural = ('users')

	def	__str__(self):
		return self.username

	def	save(self, *args, **kwargs):
		if self.pk:
			old_user = CustomUser.objects.get(pk=self.pk)
			if old_user.profile_picture and old_user.profile_picture != self.profile_picture:
				old_user.profile_picture.delete(save=False)

		super(CustomUser, self).save(*args, **kwargs)

	@property
	def	total_wins(self):
		from match.models import Match
		return Match.objects.filter(
			models.Q(user1=self, score_user1__gt=models.F('score_user2')) |
			models.Q(user2=self, score_user2__gt=models.F('score_user1'))).count()

	@property
	def	total_loses(self):
		from match.models import Match
		return Match.objects.filter(
			models.Q(user1=self, score_user1__lt=models.F('score_user2')) |
			models.Q(user2=self, score_user2__lt=models.F('score_user1'))).count()

	@property
	def	total_matches_played(self):
		from match.models import Match
		return Match.objects.filter(
			models.Q(user1=self) |
			models.Q(user2=self)).count()

	@property
	def	formatted_win_rate(self):
		total_matches = self.total_matches_played
		if total_matches > 0:
			win_rate = (self.total_wins / total_matches) * 100
			return f"{win_rate:.2f}%"
		return "N/A"

class Friendship(models.Model):
	user1 = models.ForeignKey(CustomUser, related_name='friends_initiated', on_delete=models.CASCADE)
	user2 = models.ForeignKey(CustomUser, related_name='friends_received', on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)

	class	Meta:
		unique_together = ('user1', 'user2')

	def	__str__(self):
		return f"{self.user1} is friends with {self.user2}"