import os
from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SESSION_COOKIE_AGE = 3600
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = True
SESSION_SAVE_EVERY_REQUEST = True
SECURE_SSL_REDIRECT = True



SECRET_KEY = os.getenv('JWT_SECRET_KEY')
USER_ID = os.getenv('USER_ID')
API_KEY = os.getenv('API_KEY')

DEBUG = True
ALLOWED_HOSTS = ['*', 'localhost', '0.0.0.0']

# Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django_extensions',

	'users',
	'login',
	'match',
	'tournaments',
	'ranking',

	'sslserver',
]

MIDDLEWARE = [
	'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.locale.LocaleMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',

	'ft_transcendence.middleware.middlewareJWT.JWTMiddleware',
]

SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'

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
		'ENGINE': 'django.db.backends.postgresql',
		'NAME': os.getenv('DB_NAME'),
		'USER': os.getenv('DB_USER'),
		'PASSWORD': os.getenv('DB_PASSWORD'),
		'HOST': os.getenv('DB_HOST'),
		'PORT': os.getenv('DB_PORT'),
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

LANGUAGES = [
	('en-us', 'English'),
	('pt-br', 'Português'),
]

LOCALE_PATHS = [
	os.path.join(BASE_DIR, 'locale'),
]
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static/')]
print(STATICFILES_DIRS)

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
print(STATICFILES_DIRS)


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# SMTP
EMAIL_PORT = 587
EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'transcendencenana@gmail.com'
EMAIL_HOST_PASSWORD = 'iwpl clet ncyl ycpk'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# JWEB3
BOOL_WEB3 = False
TX_HASH = os.getenv('HASH_NANA')
TX_ADDRESS = os.getenv('ADDRESS_NANA')
TX_RECEIPT = []
DEPLOYED_CONTRACT = None

CSRF_TRUSTED_ORIGINS = [
    'https://localhost:5000/*',
    'https://localhost:8000/*',
]