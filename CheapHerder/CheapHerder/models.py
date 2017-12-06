from django.db import models

class Product(models.Model):
	item_code = models.CharField(max_length=200,primary_key=True)
	product_name = models.CharField(max_length=255)
	description = models.TextField()
	quantity = models.CharField(max_length=255)
	package_size = models.CharField(max_length=255)
	gross_weight = models.CharField(max_length=255)
	category = models.CharField(max_length=200)
	created = models.DateTimeField(null=True)
	modified = models.DateTimeField(null=True)
	image_url = models.CharField(max_length=200)
	supplier_id = models.ForeignKey("auth.User", limit_choices_to={'groups__name': "Suppliers"}, null=True)
	
	# Max price from possible prices
	def max_price(self):
		return self.product_price_set.all().order_by("price_id__price").reverse().first()
	
	def __str__(self):
		return self.item_code + '-' + self.product_name


class top_product(models.Model):
	item_code = models.CharField(max_length=200,primary_key=True)
	product_name = models.CharField(max_length=255)
	description = models.TextField()
	image_url = models.CharField(max_length=200)

	class Meta:
			managed = False
			db_table='top_prod'

class Price(models.Model):
	price_id = models.AutoField(primary_key=True) 
	price = models.DecimalField(max_digits=10, decimal_places=5)
	quantity = models.IntegerField()

	def __str__(self):
		return str(self.price_id) + ': p(' + str(self.price) +') q(' + str(self.quantity) +')'

class Product_Price(models.Model):
	price_id = models.ForeignKey(Price)
	item_code = models.ForeignKey(Product)

	class Meta:
		unique_together = (("price_id", "item_code"),)

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
	org_id = models.ForeignKey("auth.User", limit_choices_to={'groups__name':"Organizations"})

class Group(models.Model):
	group_id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=200)
	product_id = models.ForeignKey(Product)
	transaction_id = models.ForeignKey(Transaction, blank = True, null = True)
	product_price = models.ForeignKey(Product_Price)
	is_open = models.BooleanField(default = True)
	members = models.ManyToManyField("auth.User", limit_choices_to={'groups__name':"Organizations"})

class Pledge(models.Model):
	group_id = models.ForeignKey(Group)
	org_id = models.ForeignKey("auth.User", limit_choices_to={'groups__name':"Organizations"})
	payment_id = models.ForeignKey(Payment)
	is_owner = models.BooleanField(default = False)

class PaymentGroupPledge(models.Model):
	username = models.CharField(max_length=200)
	amount_pledged = models.DecimalField(max_digits=10, decimal_places=5)
	time_pledged = models.DateTimeField()

	class Meta:
		managed = False

	def __str__(self):
		return str(self.username) + ' amount: ' + str(self.amount_pledged) + ' )'

