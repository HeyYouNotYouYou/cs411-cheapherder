from django.contrib.auth.models import User
from django import forms

from .models import Product, Product_Price, Price

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
		fields = ['item_code','product_name','description','quantity','package_size','gross_weight','category', 'image_url']

class PriceForm(forms.ModelForm):

	class Meta:
		model = Price
		exclude = ('price_id',)