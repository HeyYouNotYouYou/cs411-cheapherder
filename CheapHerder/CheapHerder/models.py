from django.db import models

class Supplier(models.Model):
	supplier_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	address = models.TextField()

class Organization(models.Model):
	org_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	shipping_address = models.TextField()

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
	supplier_id = models.ForeignKey(Supplier)

	def __str__(self):
		return self.sku + '-' + self.title

class Price(models.Model):
	price_id = models.AutoField(primary_key=True) 
	price = models.DecimalField(max_digits=10, decimal_places=5)
	quantity = models.IntegerField()

	def __str__(self):
		return str(self.price_id) + ': p(' + str(self.price) +') q(' + str(self.quantity) +')'

class Product_Price(models.Model):
	price_id = models.ForeignKey(Price)
	sku = models.ForeignKey(Product)

class Transaction(models.Model):
	transaction_id = models.AutoField(primary_key=True)
	amount = models.DecimalField(max_digits=10, decimal_places=5)
	description = models.TextField()
	quantity = models.IntegerField()
	status = models.CharField(max_length=100)

class Payment(models.Model):
	payment_id = models.AutoField(primary_key=True)
	created = models.DateTimeField()
	cc_expiry = models.CharField(max_length=100)
	cc_number = models.CharField(max_length=200)
	cc_ccv = models.CharField(max_length=200)
	amount = models.DecimalField(max_digits=10, decimal_places=5)

class Search_Item(models.Model):
	search_id = models.AutoField(primary_key=True)
	keyword = models.TextField()
	created = models.DateTimeField()
	org_id = models.ForeignKey(Organization)

class Group(models.Model):
	group_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	product_id = models.ForeignKey(Product)
	transaction_id = models.ForeignKey(Transaction)

class Pledges(models.Model):
	group_id = models.ForeignKey(Group)
	org_id = models.ForeignKey(Organization)
	payment_id = models.ForeignKey(Payment)





