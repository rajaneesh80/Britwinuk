from import_export import resources
from .models import stock, product

class stockResource(resources.ModelResource):
	
	class meta:
		model = stock
		skip_unchanged = True
		report_skipped = True
		exclude = ('id',)
		import_id_fields = ('barcode',)	
		feilds = ('sku','skusize','colour','buyprice','style','colournum','size','barcode','quantity',)
		export_order = ('sku','skusize','colour','buyprice','style','colournum','size','barcode','quantity',)
			
		#feilds = ('sku','skusize','color','buyprice','style','colornum','size','barcode','quantity')
		#export_order = ('sku','skusize','color','buyprice','style','colornum','size','barcode','quantity')
		
class productResource(resources.ModelResource):
	
	class meta:
		model = product

			
	