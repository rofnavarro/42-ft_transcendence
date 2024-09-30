from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.files.base import ContentFile
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _



from .forms import CustomAuthenticationForm, SetEmailForm
from users.models import CustomUser

import random
import requests
import os

import datetime
from login.jwt import create_jwt


REDIRECT_URI = 'https://localhost:8000/login/callback'

def	login_user(request):
	url = f'https://api.intra.42.fr/oauth/authorize?client_id={settings.USER_ID}&redirect_uri={REDIRECT_URI}&response_type=code'
	return redirect(url)

def	manual_login(request):
	if request.method == 'POST':
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user:
				if not user.is_online:
					login(request, user)
					send_2fa_code_email(request)
					return redirect('login:verify2fa')
				else:
					return render(request, 'login/manual_login.html', {'form': form, 'error': _('User is already logged in another device')})
			else:
				return render(request, 'login/manual_login.html', {'form': form, 'error': _('Username or password invalid. Please, try again.')})			
	else:
		form = CustomAuthenticationForm()
	return render(request, 'login/manual_login.html', {'form': form})

def	callback(request):
	code = request.GET.get('code')
	if not code:
		return render(request, 'login/error.html', {'error': _('Authorization code not received.')})

	token_url = 'https://api.intra.42.fr/oauth/token'
	token_data = {
		'grant_type': 'authorization_code',
		'client_id': settings.USER_ID,
		'client_secret': settings.API_KEY,
		'code': code ,
		'redirect_uri': REDIRECT_URI
	}

	token_response = requests.post(token_url, data=token_data)
	if token_response.status_code != 200:
		return render(request, 'login/error.html', {'error': token_response.json()})

	token_json = token_response.json()
	access_token = token_json.get('access_token')
	if not access_token:
		return render(request, 'login/error.html', {'error': _('Not possible to access token.')})

	request.session['access_token'] = access_token

	user_url = 'https://api.intra.42.fr/v2/me'

	headers = {'Authorization': f'Bearer {access_token}'}
	user_response = requests.get(user_url, headers=headers)
	user_info = user_response.json()

	username = user_info.get('login')
	last_name = user_info.get('last_name', '')
	first_name = user_info.get('usual_first_name', '') or user_info.get('first_name', '')

	user, created = CustomUser.objects.get_or_create(
		username=username,
		defaults={
			'username': username,
			'nickname': username,
			'first_name': first_name,
			'last_name': last_name,
		}
	)

	if not user.profile_picture:
		profile_pic_url = user_info.get('image', {}).get('link', '')
		if profile_pic_url:
			response = requests.get(profile_pic_url)
			if response.status_code == 200:
				_, ext = os.path.splitext(profile_pic_url)
				file_name = f'{username}_profile_picture{ext}'
				user.profile_picture.save(file_name, ContentFile(response.content))
				user.save()

	if not user.password:
		login(request, user)
		return redirect(reverse('login:set_password'))

	if not user.email:
		login(request, user)
		return redirect(reverse('login:set_email'))

	login(request, user)
	send_2fa_code_email(request)
	return redirect(reverse('login:verify2fa'))

@login_required
def	set_password(request):
	if request.method == 'POST':
		form = SetPasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('login:set_email'))
		else:
			return render(request, 'login/set_password.html', {'form': form, 'error': _('Error defining password.')})
	else:
		form = SetPasswordForm(request.user)
	return render(request, 'login/set_password.html', {'form': form})

@login_required
def	set_email(request):
	if request.method == 'POST':
		form = SetEmailForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			send_2fa_code_email(request)
			return redirect(reverse('login:verify2fa'))
		else:
			return render(request, 'login/set_email.html', {'form': form, 'error': _('Error defining e-mail.')})

	else:
		form = SetEmailForm(instance=request.user)
	return render(request, 'login/set_email.html', {'form': form})

def	logout_user(request):
	try:
		if request.method == 'POST':
			user = request.user
			user.is_online = False
			user.is_verified = False
			user.token = None
			user.save()
			request.session.flush()
			logout(request)
	except Exception as e:
		return redirect('home')
	
	return redirect('home')

def	send_2fa_code_email(request):
	code = random.randint(100000, 999999)

	request.user.verification_code = code
	request.user.save()

	subject = _('Your 2FA verification code')
	message = _('Hello %(first_name)s, \n\nYour verification code is: %(code)s.') % {'first_name': request.user.first_name, 'code': code}
	recipient = [request.user.email]
	send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, recipient)
	return

def	verify_2fa_code_email(request):
	if request.method == 'POST':
		code = request.POST.get('code')
		if not code:
			return render(request, 'login/2fa.html', {'error': _('Please insert your 2FA code: ')})
		try:
			if int(code) == request.user.verification_code:
				request.user.is_online = True
				request.user.is_verified = True
				request.user.verification_code = None

				current_time = (datetime.datetime.now() + datetime.timedelta(minutes=100)).timestamp()
				payload = {
					'username': request.user.username,
					'user_mail': request.user.email,
					'exp': current_time
				}
				token = create_jwt(payload, settings.SECRET_KEY, algorithm='HS256')
				request.session['tokenJWT'] = token
				request.user.token = token
				request.user.save()

				return redirect('users:wanna_play', username=request.user.username)
			else:
				return render(request, 'login/2fa.html', {'error': _('Incorrect code.')})
		except ValueError:
			return render(request, 'login/2fa.html', {'error': _('Incorrect code.')})
	return render(request, 'login/2fa.html')