from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group

from .forms import SupplierForm, OrganizationForm

class Index(TemplateView):
    template_name = "index.html"
		
class SupplierFormView(View):
	form_class = SupplierForm
	template_name = "registration_supp_form.html"

	#display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	#process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#normalize data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()

			# add user to correct group
			g = Group.objects.get(name='Suppliers') 
			g.user_set.add(user)

			# authenticate then login supplier

			user = authenticate(username = username,password = password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('index')

		return render(request, self.template_name, {'form': form})

class OrganizationFormView(View):
	form_class = OrganizationForm
	template_name = "registration_org_form.html"

	#display blank form
	def get(self, request):
		form = self.form_class(None)
		return render(request, self.template_name, {'form': form})

	#process form data
	def post(self, request):
		form = self.form_class(request.POST)

		if form.is_valid():

			user = form.save(commit=False)

			#normalize data
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user.set_password(password)
			user.save()


			# add user to correct group
			g = Group.objects.get(name='Organizations') 
			g.user_set.add(user)

			# authenticate then login supplier

			user = authenticate(username = username,password = password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('index')

		return render(request, self.template_name, {'form': form})


def SuppLogin(request):

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('index')
			else:
				return render(request, 'login_supp_form.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'login_supp_form.html', {'error_message': 'Invalid login'})
	return render(request, 'login_supp_form.html')

def OrgLogin(request):

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('index')
			else:
				return render(request, 'login_org_form.html', {'error_message': 'Your account has been disabled'})
		else:
			return render(request, 'login_org_form.html', {'error_message': 'Invalid login'})
	return render(request, 'login_org_form.html')
