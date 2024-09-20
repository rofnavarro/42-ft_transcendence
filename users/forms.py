from django import forms
from users.models import CustomUser

class	EditNicknameForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['nickname']

class	ProfilePictureForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['profile_picture']
		widgets = {
			'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control'}),
		}