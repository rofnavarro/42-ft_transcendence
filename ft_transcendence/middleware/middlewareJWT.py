from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse # reverse converte o pathname para a url
from django.conf import settings
from login.jwt import decode_jwt
from login.views import logout_user
import datetime

class JWTMiddleware:
	def __init__(self, get_response):
		self.get_response = get_response

	def __call__(self, request):

		self.process_view(request, None, None, None)

		response = self.get_response(request)

		return response

	def force_logout(self, request):
		user = request.user
		user.is_online = False
		user.is_verified = False
		user.token = None
		user.save()
		request.session.flush()
		logout(request)
		return redirect(reverse('home'))

	def verify_jwt(self, request):
		try:
			session_token = request.session['tokenJWT']
			if session_token == request.user.token:
				payload = decode_jwt(session_token, settings.SECRET_KEY, algorithm='HS256')
				
				if payload['exp'] < datetime.datetime.now().timestamp():
					self.force_logout(request)
					return redirect(reverse('home'))

		except Exception as e:
			self.force_logout(request)
			
			return redirect(reverse('home'))

		return request

	def process_view(self, request, view_func, view_args, view_kwargs):
		paths = ['/admin/', '/login/', '/about/', '/ranking/']

		if request.path == '/' or request.path.startswith(tuple(paths)):
			pass
		else:
			if request.user.is_authenticated:
				self.verify_jwt(request)
			else:
				return redirect(reverse('home'))
		return None