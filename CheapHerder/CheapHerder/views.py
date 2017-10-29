from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

from .forms import SupplierForm

class Index(TemplateView):
    template_name = "index.html"
		
class SupplierFormView(View):
	form_class = SupplierForm
	template_name = "registration_form.html"

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

			# authenticate then login supplier

			user = authenticate(username = username,password = password)
			if user is not None:
				if user.is_active:
					login(request, user)
					return redirect('index')

		return render(request, self.template_name, {'form': form})