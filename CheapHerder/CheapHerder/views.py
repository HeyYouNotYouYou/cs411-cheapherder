from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.models import *
from .models import Product
from .forms import SupplierForm, OrganizationForm, ProductForm

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
					return redirect('supplier_products')

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



def create_product(request):
	form = ProductForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		product = form.save(commit=False)
            # album.user = request.user
            # album.album_logo = request.FILES['album_logo']
            # file_type = album.album_logo.url.split('.')[-1]
            # file_type = file_type.lower()
            # if file_type not in IMAGE_FILE_TYPES:
            #     context = {
            #         'album': album,
            #         'form': form,
            #         'error_message': 'Image file must be PNG, JPG, or JPEG',
            #     }
                return render(request, 'create_product.html', context)
        	# album.save()
            # return render(request, 'detail.html', {'album': album})
        context = {
            "form": form,
        }
        return render(request, 'create_product.html', context)
def delete_product(request, product_id):
    product = Product.objects.get(sku=product_id)
    product.delete()
    products = Product.objects.filter(supplier=request.user)
    return render(request, 'supplier_products.html', {'products': products})

def update_product(request, product_id):
	return redirect('index')


def SuppLogin(request):

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				login(request, user)
				return redirect('supplier_products')
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

def logout_user(request):
    logout(request)
    if is_Supplier(request.user):
    	form = SupplierForm(request.POST or None)
    else:
    	form = OrganizationForm(request.POST or None)
    context = {
        "form": form,
    }
    return render(request, 'index.html', context)

def supplier_products(request):
	if not request.user.is_authenticated():
		return render(request, 'index.html')
	else:
		products = Product.objects.filter(supplier_id=request.user)
		query = request.GET.get("q")
        if query:
            products = products.filter(
                Q(description__icontains=query) |
                Q(title__icontains=query)
            ).distinct()
            
            return render(request, 'supplier_products.html', {'products': products})
        else:
            return render(request, 'supplier_products.html', {'products': products})


def product_detail(request, product_id):
    if not request.user.is_authenticated():
        return render(request, 'index.html')
    else:
        user = request.user
        product = get_object_or_404(Product, sku=product_id)
        return render(request, 'product_detail.html', {'product': product, 'user': user})

def is_Supplier(user):
    return user.groups.filter(name='Suppliers').exists()

def is_Organization(user):
	return user.groups.filter(name='Organizations').exists()