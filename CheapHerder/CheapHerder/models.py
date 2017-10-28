from django.db import models

class Product(models.Model):
	sku = models.CharField(max_length=200, primary_key=True)
	upc = models.CharField(max_length=200)
	title = models.CharField(max_length=200)
	description = models.TextField()
	p_type = models.CharField(max_length=255)
	brand = models.CharField(max_length=255)
	colors = models.CharField(max_length=255)
	materials = models.CharField(max_length=255)
	attributes = models.CharField(max_length=255)
	tags = models.CharField(max_length=255)
	category_id = models.IntegerField()
	unit_weight = models.DecimalField(max_digits=10, decimal_places=5)
	category = models.CharField(max_length=200)
	subcategory_id = models.IntegerField()
	subcategory = models.CharField(max_length=200)
	inventory = models.CharField(max_length=200)
	created = models.DateTimeField()
	modified = models.DateTimeField()
	image_url = models.CharField(max_length=200)
	supplier_id = models.CharField(max_length=200)


class Price(models.Model):
	price_id = models.AutoField(primary_key=True) 
	price = models.DecimalField(max_digits=10, decimal_places=5)
	quantity = models.IntegerField()

class Product_Price(models.Model):
	price_id = models.ForeignKey(Price)
	sku = models.ForeignKey(Product)