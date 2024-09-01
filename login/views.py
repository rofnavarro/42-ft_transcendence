from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
import requests
from .jwt import *
from users.models import CustomUser


USER_ID = 'u-s4t2ud-a782b48361e73b59a6d5cbec76768c8aafa00b43e48aea014b90da7efb556ce5'
API_KEY = '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'
REDIRECT_URI = 'http://localhost:8000/login/callback'

SECRET_KEY = '42TR4NSC3ND3NC3'

def login_user(request):
	url = f'https://api.intra.42.fr/oauth/authorize?client_id={USER_ID}&redirect_uri={REDIRECT_URI}&response_type=code'
	return redirect(url)

def callback(request):
	code = request.GET.get('code')
	token_url = 'https://api.intra.42.fr/oauth/token'
	token_data = {
		'grant_type': 'authorization_code',
		'client_id': USER_ID,
		'client_secret': API_KEY,
		'code': code ,
		'redirect_uri': REDIRECT_URI
	}

	# jwt_token = create_jwt(token_data, SECRET_KEY)

	token_response = requests.post(token_url, data=token_data)
	if token_response.status_code != 200:
		return render(request, 'login/error.html', {'error': token_response.json()})

	token_json = token_response.json()
	access_token = token_json.get('access_token')

	request.session['access_token'] = access_token

	user_url = 'https://api.intra.42.fr/v2/me'
	headers = {'Authorization': f'Bearer {access_token}'}
	user_response = requests.get(user_url, headers=headers)
	user_info = user_response.json()

	email = user_info.get('email')
	username = user_info.get('login')
	last_name = user_info.get('last_name', '')
	first_name = user_info.get('usual_first_name', '')

	if not first_name:
		first_name = user_info.get('first_name', '')

	user, created = CustomUser.objects.get_or_create(
		email=email,
		defaults={
			'username': username,
			'first_name': first_name,
			'last_name': last_name,
		}
	)

	if not created:
		user.username = username
		user.first_name = first_name
		user.last_name = last_name
		user.save()

	login(request, user)

	context = {
		'user_info': user,
	}

	# print(user_info)

	return redirect(f'/users/profile/{username}')

def logout_user(request):
	access_token = request.session.get('access_token')
	if access_token:
		revoke_url = 'https://api.intra.42.fr/oauth/revoke'
		revoke_data = {
			'token': access_token,
			'client_id': USER_ID,
			'client_secret': API_KEY,
		}
		requests.post(revoke_url, data=revoke_data)
	request.session.pop('access_token', None)
	logout(request)
	request.session.flush()
	return redirect('home')
