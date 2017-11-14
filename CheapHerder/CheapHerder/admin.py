# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Product)
admin.site.register(Price)
admin.site.register(Product_Price)
admin.site.register(Transaction)
admin.site.register(Payment)
admin.site.register(Pledge)
admin.site.register(Search_Item)
admin.site.register(Group)
