from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
	def confirm_login_allowed(self, user):
		if not user.is_active:
			raise forms.ValidationError("Esta conta está inativa.", code='inactive')
		if user.is_superuser:
			raise forms.ValidationError("O superusuário não pode logar por este formulário.", code='no_superuser')

	def get_invalid_login_error(self):
		return forms.ValidationError("Usuário ou senha incorretos. Tente novamente.", code='invalid_login')
