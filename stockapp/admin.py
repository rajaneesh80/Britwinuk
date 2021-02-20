from django.contrib import admin
from import_export.admin import ImportExportModelAdmin, ExportActionModelAdmin, ImportExportActionModelAdmin, ExportActionMixin
from django import forms
from .models import File ,stock, product
from .resources import stockResource,productResource
from import_export import resources

# Register your models here.

# admin.site.register(stock)
# admin.site.register(File)

#@admin.register(stock) 
#class stockAdmin(ExportActionMixin, admin.ModelAdmin, ImportExportModelAdmin, ImportExportActionModelAdmin):


class stockAdmin(ExportActionModelAdmin, ImportExportModelAdmin  ): #ExportActionModelAdmin, ImportExportModelAdmin
	list_display = ('sku','skusize','colour','buyprice','style','colournum','size','barcode','quantity')
	list_per_pImportExportModelAdminage = 10
	# resource_class= stockResource
	# exclude = ('id',)
	# import_id_fields = ('barcode',)	
	# feilds = ('sku','skusize','color','buyprice','style','colornum','size','barcode','quantity')
	
class productAdmin(  ExportActionModelAdmin, ImportExportModelAdmin):#ExportActionModelAdmin, ImportExportModelAdmin
	list_display = ('sku','skusize','style','colournum','size','colour','buyprice','sellprice','buycurrency','costpriceowncurrency','costcurrency','barcode','collection','brandname','season','sizerange','article')
	
	list_per_page = 10

admin.site.register(stock,stockAdmin)
admin.site.register(product, productAdmin)