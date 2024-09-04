from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import BaseUserManager

class	CustomUserManager(BaseUserManager):
	def create_user(self, email, username, password=None, **extra_fields):
		if not email:
			raise ValueError(gettext_lazy('Necessita de um email'))
		if not username:
			raise ValueError(gettext_lazy('Necessita de um nome de usuário'))
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, **extra_fields)
		user.set_unusable_password()
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
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(gettext_lazy('email address'), unique=True)
	first_name = models.CharField(gettext_lazy('first name'), max_length=30, blank=True)
	last_name = models.CharField(gettext_lazy('last name'), max_length=30, blank=True)
	
	date_joined = models.DateTimeField(gettext_lazy('date joined'), default=timezone.now)
	is_active = models.BooleanField(gettext_lazy('active'), default=True)
	
	is_staff = models.BooleanField(gettext_lazy('staff status'), default=False)
	is_superuser = models.BooleanField(gettext_lazy('superuser status'), default=False)

	is_online = models.BooleanField(default=False)
	last_online = models.DateTimeField(default=timezone.now)
	
	friends = models.ManyToManyField('self', symmetrical=False, through='Friendship')

	objects = CustomUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = []


	class	Meta:
		verbose_name = gettext_lazy('user')
		verbose_name_plural = gettext_lazy('users')

	def	__str__(self):
		return self.username

	@property
	def total_wins(self):
		from match.models import Match
		return Match.objects.filter(
			models.Q(user1=self, score_user1__gt=models.F('score_user2')) |
			models.Q(user2=self, score_user2__gt=models.F('score_user1'))
		).count()

	@property
	def total_loses(self):
		from match.models import Match
		return Match.objects.filter(
			models.Q(user1=self, score_user1__lt=models.F('score_user2')) |
			models.Q(user2=self, score_user2__lt=models.F('score_user1'))
		).count()

	@property
	def total_matches_played(self):
		from match.models import Match
		return Match.objects.filter(
			models.Q(user1=self) |
			models.Q(user2=self)
		).count()

	@property
	def formatted_win_rate(self):
		total_matches = self.total_matches_played
		if total_matches > 0:
			win_rate = (self.total_wins / total_matches) * 100
			return f"{win_rate:.2f}%"
		return "N/A"

class	Friendship(models.Model):
	user1 = models.ForeignKey(CustomUser, related_name='friendships', on_delete=models.CASCADE)
	user2 = models.ForeignKey(CustomUser, related_name='+', on_delete=models.CASCADE)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user1', 'user2')

	def __str__(self):
		return f"{self.user1.username} is friends with {self.user2.username}"
