from django.contrib.auth.models import User
from django import forms

class SupplierForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)


	class Meta:
		model = User
		fields = ['username', 'email', 'password']
			
class OrganizationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	

	class Meta:
		model = User
		fields = ['username', 'email', 'password']