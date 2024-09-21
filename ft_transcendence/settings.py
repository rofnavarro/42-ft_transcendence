import os
from pathlib import Path
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

LOGIN_URL = '/login'

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SECURE = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6waaegtj9iw2dh7plax#^2w+e$s(ig$by=v9zdrvavq9u5hf8^'

# SECURITY WARNING: don't run with debug turned on in production!
# TODO: trocar para o ip da maquina que vai rodar o servidor e mudar o DEBUG para False
DEBUG = True
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',

	'sslserver',

	'login',
	'match',
	'ranking',
	'users',
	'tournaments'
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ft_transcendence.urls'

TEMPLATES = [
	{
		'BACKEND': 'django.template.backends.django.DjangoTemplates',
		'DIRS': ['templates'],
		'APP_DIRS': True,
		'OPTIONS': {
			'context_processors': [
				'django.template.context_processors.debug',
				'django.template.context_processors.request',
				'django.contrib.auth.context_processors.auth',
				'django.contrib.messages.context_processors.messages',
			],
		},
	},
]

WSGI_APPLICATION = 'ft_transcendence.wsgi.application'

AUTH_USER_MODEL = 'users.CustomUser'

# Database
DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',

		# 'NAME': os.getenv('DB_NAME'),
		# 'USER': os.getenv('DB_USER'),
		# 'PASSWORD': os.getenv('DB_PASSWORD'),
		# 'HOST': os.getenv('DB_HOST'),
		# 'PORT': os.getenv('DB_PORT'),
	}
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
	{
		'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
	},
	{
		'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
	},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'transcendencenana@gmail.com'
EMAIL_HOST_PASSWORD = 'iwpl clet ncyl ycpk'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
