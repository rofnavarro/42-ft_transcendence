from django.shortcuts import redirect, render
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import SetPasswordForm, AuthenticationForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.files.base import ContentFile

from .forms import CustomAuthenticationForm
from users.models import CustomUser

import requests
import os

USER_ID = 'u-s4t2ud-a782b48361e73b59a6d5cbec76768c8aafa00b43e48aea014b90da7efb556ce5'
API_KEY = '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'
REDIRECT_URI = 'http://localhost:8000/login/callback'

def	login_user(request):
	url = f'https://api.intra.42.fr/oauth/authorize?client_id={USER_ID}&redirect_uri={REDIRECT_URI}&response_type=code'
	return redirect(url)

def	manual_login(request):
	if request.method == 'POST':
		form = CustomAuthenticationForm(request, data=request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			if user:
				if not user.is_online:
					user.is_online = True
					user.save()
					login(request, user)
					return redirect('/users/profile/' + user.username)
				else:
					return render(request, 'login/manual_login.html', {'form': form, 'error': 'Usuário já está logado em outro dispositivo.'})
			else:
				return render(request, 'login/manual_login.html', {'form': form, 'error': 'Usuário ou senha inválido(a).'})			
	else:
		form = CustomAuthenticationForm()
	return render(request, 'login/manual_login.html', {'form': form})

def	callback(request):
	code = request.GET.get('code')
	if not code:
		return render(request, 'login/error.html', {'error': 'Código de autorização não recebido.'})

	token_url = 'https://api.intra.42.fr/oauth/token'
	token_data = {
		'grant_type': 'authorization_code',
		'client_id': USER_ID,
		'client_secret': API_KEY,
		'code': code ,
		'redirect_uri': REDIRECT_URI
	}

	token_response = requests.post(token_url, data=token_data)
	if token_response.status_code != 200:
		return render(request, 'login/error.html', {'error': token_response.json()})

	token_json = token_response.json()
	access_token = token_json.get('access_token')
	if not access_token:
		return render(request, 'login/error.html', {'error': 'Não foi possível acessar o token.'})

	request.session['access_token'] = access_token

	user_url = 'https://api.intra.42.fr/v2/me'
	headers = {'Authorization': f'Bearer {access_token}'}
	user_response = requests.get(user_url, headers=headers)
	user_info = user_response.json()

	email = user_info.get('email')
	username = user_info.get('login')
	last_name = user_info.get('last_name', '')
	first_name = user_info.get('usual_first_name', '') or user_info.get('first_name', '')

	user, created = CustomUser.objects.get_or_create(
		email=email,
		defaults={
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
		}
	)
	profile_pic_url = user_info.get('image', {}).get('link', '')
	if profile_pic_url:
		response = requests.get(profile_pic_url)
		if response.status_code == 200:
			_, ext = os.path.splitext(profile_pic_url)
			file_name = f'{username}_profile_picture.{ext}'
			user.profile_picture.save(file_name, ContentFile(response.content))
			user.save()

	if not user.password:
		if not user.is_online:
			user.save()
			login(request, user)
			return redirect(reverse('login:set_password'))
		else:
			print(f"User {username} is already online.")
			return render(request, 'login/error.html', {'error': 'Usuário já está logado em outro dispositivo.'})

	if not user.is_online:
		user.is_online = True
		user.save()
		login(request, user)
		return redirect(reverse('users:profile', kwargs={'username': username}))
	else:
		return render(request, 'login/error.html', {'error': 'Usuário já está logado em outro dispositivo.'})

@login_required
def	set_password(request):
	if request.method == 'POST':
		form = SetPasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			return redirect(reverse('users:profile', kwargs={'username': request.user.username}))
	else:
		form = SetPasswordForm(request.user)
		
	return render(request, 'login/set_password.html', {'form': form})

@login_required
def	logout_user(request):
	user = request.user
	user.is_online = False
	user.save()

	logout(request)
	request.session.flush()
	return redirect('home')
