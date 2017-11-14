"""CheapHerder URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from .views import *

urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^supplier/register/$', SupplierFormView.as_view(), name ='supp_register'),
    url(r'^supplier/login/$', SuppLogin, name ='supp_login'),
    url(r'^organization/register/$', OrganizationFormView.as_view(), name ='org_register'),
    url(r'^organization/login/$', OrgLogin, name ='org_login'),
    url(r'^logout_user/$', logout_user, name='logout_user'),
    url(r'^supplier/products/$', supplier_products, name ='supplier_products'),
    url(r'^supplier/create_product/$', create_product, name='create_product'),
    url(r'^supplier/(?P<product_id>[0-9]+)/delete_product/$', delete_product, name='delete_product'),
    url(r'^supplier/(?P<product_id>[0-9]+)/$', product_detail, name='product_detail'),
    url(r'^supplier/(?P<product_id>[0-9]+)/update_product/$', update_product, name='update_product'),

]
