from django import forms
from django.contrib.auth.forms import AuthenticationForm
from users.models import CustomUser
from django.utils.translation import gettext_lazy

class	CustomAuthenticationForm(AuthenticationForm):
	def	confirm_login_allowed(self, user):
		if not user.is_active:
			raise forms.ValidationError("This account is inactive.", code='inactive')
		if user.is_superuser:
			raise forms.ValidationError(gettext_lazy("Superuser cannot login from this form."), code='no_superuser')

	def	get_invalid_login_error(self):
		return forms.ValidationError(gettext_lazy("Username or password is incorrect. Please try again."), code='invalid_login')

class	SetEmailForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['email']
		labels = {
			'email': 'New E-mail ',
		}
		widgets = {
			'email': forms.EmailInput(attrs={'class': 'form-control'}),
		}

	def __init__(self, *args, **kwargs):
		super(SetEmailForm, self).__init__(*args, **kwargs)
		self.fields['email'].required = True

	def clean_email(self):
		email = self.cleaned_data.get('email')
		if CustomUser.objects.filter(email=email).exists():
			raise forms.ValidationError('This e-mail address is already in use.')
		return email
