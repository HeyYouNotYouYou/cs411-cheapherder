from django.views.generic import TemplateView, View, ListView, DetailView
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from .models import *
from .models import Group as ProdGroup
from .forms import SupplierForm, OrganizationForm, ProductForm, PriceForm
from django.forms.formsets import formset_factory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

import random

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


def create_prices(request, product_id):
		return redirect('index')

def create_product(request):
	if not request.user.is_authenticated():
		return redirect('index')
	else:
		form = ProductForm(request.POST or None, request.FILES or None)

		if form.is_valid():
			product = form.save(commit=False)
			product.supplier_id = request.user
			product.save()

		context = {
			"form": form,
		}
		return render(request, 'create_product.html', context)

def delete_product(request, product_id):
	product = Product.objects.get(item_code=product_id)
	product.delete()
	return redirect('supplier_products')


def update_product(request, product_id):
	instance = get_object_or_404(Product, item_code=product_id)
	form = ProductForm(request.POST or None, instance=instance)
	if form.is_valid():
		form.save()
		return redirect('supplier_products')
	return render(request, 'update_product.html', {'form': form})

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
				return redirect('org_home')
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
		page = request.GET.get('page', 1)
		query = request.GET.get("q")
		paginator = Paginator(products, 2)

		if query:
			products = products.filter(
				Q(description__icontains=query) |
				Q(product_name__icontains=query)
			).distinct()
		else:
			try:
				products = paginator.page(page)
			except PageNotAnInteger:
				products = paginator.page(1)
			except EmptyPage:
				products = paginator.page(paginator.num_pages)
			return render(request, 'supplier_products.html', {'products': products})
		return render(request, 'supplier_products.html', {'products': products})


def SuppProductDetail(request, product_id):
    if not request.user.is_authenticated():
        return render(request, 'index')
    else:
        user = request.user
        product = get_object_or_404(Product, pk=product_id)
        return render(request, 'product_detail.html', {'product': product, 'user': user})


# home page and top picks - just a random sample - we can implement a better algorithm later
class OrgHome(TemplateView):
    template_name = "org_home.html"
    def get_context_data(self, **kwargs):
	context = super(OrgHome, self).get_context_data(**kwargs)
	context["products"] = random.sample(Product.objects.all(), 4)
	return context
    
# Main list of products - simple filtering for search and category selection
class OrgProducts(ListView):
    
    model = Product
    template_name = "org_products.html"
    paginate_by = 24 # I love django
    
    def get_context_data(self, **kwargs):
	context = super(OrgProducts, self).get_context_data(**kwargs)
	context['catgeories'] = Product.objects.order_by("category").values_list("category", flat = True).distinct()
	context['query'] = self.request.GET.get("q", "")
	context['category'] = self.request.GET.get("category", "")
	return context
    
    # Filtering and search
    def get_queryset(self):
	query = self.request.GET.get("q", None)
	category = self.request.GET.get("category", None)
	original = super(OrgProducts, self).get_queryset().order_by("created")
	if query:
	    return original.filter(product_name__icontains = query)
	elif category:
	    return original.filter(category = category)
	else:
	    return original
    
# Product detail pages - simple post for creating new groups
class OrgProductDetail(DetailView):
    template_name = "product_single.html"
    model = Product
    
    # The input needs to be cleaned before being used in a model creation
    def post(self, request, **kwargs):
	name = request.POST.get("name", None)
	pk = request.POST.get("product_pk", None)
	if not name or not pk: return redirect(request.get_full_path())
	g = ProdGroup(name = name, product_id = get_object_or_404(Product, pk = pk))
	g.save()
	g.members.add(request.user)
	return redirect(request.get_full_path())
    
    def get_context_data(self, **kwargs):
	context = super(OrgProductDetail, self).get_context_data(**kwargs)
	context["groups"] = self.object.group_set.filter(is_open = True)
	return context

class OrgGroupDetail(DetailView):
    model = ProdGroup
    template_name = "group_single.html"
    


'''********** HELPER FUNCTIONS ************ '''

def is_Supplier(user):
    return user.groups.filter(name='Suppliers').exists()

def is_Organization(user):
	return user.groups.filter(name='Organizations').exists()