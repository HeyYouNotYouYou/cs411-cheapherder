from django.contrib.auth.models import User
from django import forms

from .models import Product

class SupplierForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	address = forms.CharField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'address']
			
class OrganizationForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	shipping_address = forms.CharField()

	class Meta:
		model = User
		fields = ['username', 'email', 'password', 'shipping_address']


class ProductForm(forms.ModelForm):

	class Meta:
		model = Product
		fields = ['item_code','product_name']