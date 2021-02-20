from django.db import models




# Create your models here.

class File(models.Model):
	file = models.FileField(upload_to='static/TEMP/',blank=False, null=False)
def __str__(self):
	return self.file.name



class product(models.Model):
	"""docstring for stock"""
	sku = models.CharField( max_length=20, null=False, blank=False )
	skusize = models.CharField( max_length=20, null=False, blank=False )
	style = models.CharField( max_length=20, null=False, blank=False )
	colournum = models.CharField( max_length=20, null=False, blank=False ) 
	size = models.CharField( max_length=20, null=False, blank=False )
	colour = models.CharField( max_length=60, null=False, blank=False )
	buyprice = models.FloatField(null=False, default=0.0)
	sellprice = models.FloatField(null=False, default=0.0)
	buycurrency = models.CharField( max_length=20, null=False, blank=False )
	costpriceowncurrency =models.FloatField(null=False, default=0.0)
	costcurrency = models.CharField( max_length=20, null=False, blank=False )
	barcode = models.CharField( max_length=100, null=False, blank=False, unique=True)
	collection = models.CharField( max_length=200, null=False, blank=False )
	brandname = models.CharField( max_length=200, null=False, blank=False )
	season = models.CharField( max_length=20, null=False, blank=False )
	sizerange = models.CharField( max_length=20, null=False, blank=False )
	article = models.CharField( max_length=200, null=False, blank=False )


	class Meta:
		ordering = ["id"]

class stock(models.Model):
	"""docstring for stock"""
	# _id = models.AutoField(primary_key=True)
	sku = models.CharField( max_length=20, null=False, blank=False )
	skusize = models.CharField( max_length=25, null=False, blank=False)
	colour = models.CharField( max_length=50, null=False, blank=False)
	buyprice= models.FloatField(null=False, default=0.0)
	style = models.CharField( max_length=25, null=False, blank=False)
	colournum = models.IntegerField(null=False, default=0)
	size = models.CharField( max_length=25, null=False, blank=False)
	#barcode = models.CharField( max_length=100, null=False, blank=False, unique=True)
	barcode = models.ForeignKey(product, to_field="barcode", db_column="barcode", on_delete=models.CASCADE)
	quantity = models.IntegerField(null=False, default=0)

# def __str__(self):
# 	return str('%s object' % self.barcode.barcode)	

