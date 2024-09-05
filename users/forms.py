from django import forms
from users.models import CustomUser

class EditNicknameForm(forms.ModelForm):
	class Meta:
		model = CustomUser
		fields = ['nickname']
