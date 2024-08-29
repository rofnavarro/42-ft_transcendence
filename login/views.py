from django.shortcuts import redirect, render
import requests

USER_ID = 'u-s4t2ud-b9272d3f2544b1893d54288c9654aef2802f4f7773dc604528c832a6a0fc9b5c'
API_KEY = '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'
REDIRECT_URI = 'http://localhost:8000/login/callback'


def login(request):
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
	token_response = requests.post(token_url, data=token_data)
	if token_response.status_code != 200:
		return render(request, 'auth42/error.html', {'error': token_response.json()})
	token_json = token_response.json()
	access_token = token_json.get('access_token')

	user_url = 'https://api.intra.42.fr/v2/me'
	headers = {'Authorization': f'Bearer {access_token}'}
	user_response = requests.get(user_url, headers=headers)
	user_info = user_response.json()

	context = {
		'user_info': user_info,
	}

	return render(request, 'login/login.html', context)