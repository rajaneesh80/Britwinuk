from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render
#from .forms import UploadFileForm
#import openpyxl
from .models import stock, product
from django.db import DatabaseError, IntegrityError
from .resources import stockResource, productResource
from django.contrib import messages
from tablib import Dataset
import tablib

from django.views.generic.list import ListView
from django.views import generic
from django.core.paginator import Paginator





class StockListView(generic.ListView):
    model = stock
    stocklist = stock.objects.all()
    #dataset = stockResource().export(stocklist)
    #dataset.xls
    template_name = 'stock_list.html' 
    paginate_by = 10
    st_list = Paginator(stocklist, 10)
    #response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    #response = HttpResponse(dataset.xls, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #response['Content-Disposition'] = 'attachment; filename="StockList.xls"'

class ProductListView(generic.ListView):
    model = product
    productlist = product.objects.all()
    #dataset = productResource().export(productlist)
    #dataset.xls
    template_name = 'product_list.html' 
    paginate_by = 10
    st_list = Paginator(productlist, 10)
    #response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    #response = HttpResponse(dataset.xls, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #response['Content-Disposition'] = 'attachment; filename="ProductList.xls"'

def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        #file_format = request.POST['file-format']
        model_name = request.POST['modelname']
        if model_name == 'Product':
            model = product
            productlist = product.objects.all()
            all_fields = product._meta.fields
            all_fields = [f.name for f in product._meta.get_fields()]
            #@print(all_fields)
            product_resource = productResource()
            dataset = product_resource.export(productlist)
            print(all_fields)
            headers = (tuple([ 'id', 'sku', 'skusize', 'style', 'colournum', 'size', 'colour', 'buyprice', 'sellprice', 'buycurrency', 'costpriceowncurrency', 'costcurrency', 'barcode', 'collection', 'brandname', 'season', 'sizerange', 'article']))
            data = []
            data = tablib.Dataset(*data, headers=headers)
            #productlist = product.objects.all()
            for myproduct in productlist:
                data.append(( myproduct.id, myproduct.sku, myproduct.skusize, myproduct.style, myproduct.colournum, myproduct.size, myproduct.colour, myproduct.buyprice, myproduct.sellprice, myproduct.buycurrency, myproduct.costpriceowncurrency, myproduct.costcurrency, myproduct.barcode, myproduct.collection, myproduct.brandname, myproduct.season, myproduct.sizerange, myproduct.article))
            #if file_format == 'XLS (Excel)':
            #dataset.xls
            response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="ProductList.xls"'
            return response   
        if model_name == 'Inventory':
            model = stock
            stocklist = stock.objects.all()
            all_fields = [f.name for f in stock._meta.get_fields()]
            #print(all_fields)
            stock_resource = stockResource()
            dataset = stock_resource.export(stocklist)
            headers = tuple(all_fields)
            data = []
            data = tablib.Dataset(*data, headers=headers)
            #productlist = product.objects.all()
            for mystock in stocklist:
                data.append((mystock.id, mystock.sku, mystock.skusize, mystock.colour, mystock.buyprice, mystock.style, mystock.colournum, mystock.size, mystock.barcode.barcode, mystock.quantity))
            #if file_format == 'XLS (Excel)':
            #dataset.xls
            response = HttpResponse(data.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="Stocklist.xls"'
            return response 
    return render(request, 'export.html')

# Create your views here.
def home(request):
    my_name="BritwinUK Shoes Inventory"
    return render(request,"home.html",{"bob": my_name})

# def about(request):
#     return render(request,"about.html",{})

 

def del_stock(request):

    if request.method == 'POST':
        stock_resource = stockResource()
        dataset = Dataset()
        new_stock = request.FILES['myfile']

        #storage = messages.get_messages(request)
        #storage.used = True
        if not new_stock.name.endswith('xlsx'):
            messages.info(request, 'Wrong File format - Please select the correct Excel File format')
            return render (request,'delstock.html')
        imported_data = dataset.load(new_stock.read(),format='xlsx')
        #stock.objects.all().delete()

        if not dataset.headers == list(['id', 'sku', 'skusize', 'colour', 'buyprice', 'style', 'colournum', 'size', 'barcode', 'quantity']):
            messages.info(request, 'Please Upload the correct File with Header!')
            return render (request,'delstock.html')
        
        for data in imported_data:
            updated_id = stock.objects.filter(barcode=data[8]).values_list('id', flat=True)
            old_qty = stock.objects.filter(barcode=data[8]).values_list('quantity', flat=True)
            if not updated_id: 
                messages.info(request, 'There is No corresponding Inventory in the sheet for Barcode - '+ str(data[8]) )
                return render(request, 'delstock.html')
            else:
                print(updated_id[0])
                value = stock(updated_id[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],old_qty[0]-data[9])

            try:
                value.save()
            except DatabaseError as e:
                messages.info(request, 'There is No corresponding Inventory in the sheet!! ')
                return render(request, 'delstock.html')
        #storage.used = True
        messages.info(request, 'File Uploaded SuccessFully!')
    return render(request, 'delstock.html')

def add_stock(request):

    if request.method == 'POST':
        stock_resource = stockResource()
        dataset = Dataset()
        new_stock = request.FILES['myfile']

        
        #storage = messages.get_messages(request)
        #storage.used = True

        if not new_stock.name.endswith('xlsx'):
            #storage.used = True
            messages.info(request, 'Wrong File format - Please select the correct Excel File format')
            return render (request,'addstock.html')
        imported_data = dataset.load(new_stock.read(),format='xlsx')
        #print(dataset.headers)  
        #print(len(dataset.headers))  
              
        #stock.objects.all().delete()
        if not dataset.headers == list(['id', 'sku', 'skusize', 'colour', 'buyprice', 'style', 'colournum', 'size', 'barcode', 'quantity']):
            messages.info(request, 'Please Upload the correct File with Header!')
            return render (request,'addstock.html')
        for data in imported_data:
            #print(type(data))
            try:
                updated_id = stock.objects.filter(barcode=data[8]).values_list('id', flat=True)
                old_qty = stock.objects.filter(barcode=data[8]).values_list('quantity', flat=True)
            except exception as e:
                messages.info(request, 'There is an Error in the sheet!! ')
                return render(request, 'addstock.html')
            if not updated_id: 
                #print(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8])
                value = stock(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9])
                #value = stock(sku = data[0], skusize = data[1], colour = data[2], buyprice = data[3], style = data[4], colournum = data[5], size = data[6], barcode = product.objects.filter(barcode=data[7]).values_list('barcode', flat=True), quantity = data[8])
            else:
                value = stock(updated_id[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9]+old_qty[0])
            try:
                value.save()
            except IntegrityError as e:
                messages.info(request, 'There is no associated product with barcode in the sheet!! ')
                return render(request, 'addstock.html')
        #storage.used = True
        messages.info(request, 'File Uploaded SuccessFully!')
    return render(request, 'addstock.html')

def add_product(request):

    if request.method == 'POST':
        product_resource = productResource()
        dataset = Dataset()
        new_product = request.FILES['myfile']

        
        #storage = messages.get_messages(request)
        #storage.used = True

        if not new_product.name.endswith('xlsx'):
            #storage.used = True
            messages.info(request, 'Wrong File format - Please select the correct Excel File format')
            return render (request,'addproduct.html')
        imported_data = dataset.load(new_product.read(),format='xlsx')
        #print(dataset.headers)  
        #print(len(dataset.headers))  
              
        #stock.objects.all().delete()
        if not dataset.headers == list(['id', 'sku', 'skusize', 'style', 'colournum', 'size', 'colour', 'buyprice', 'sellprice', 'buycurrency', 'costpriceowncurrency', 'costcurrency', 'barcode', 'collection', 'brandname', 'season', 'sizerange', 'article']):
            messages.info(request, 'Please Upload the correct File with Header!')
            return render (request,'addproduct.html')
        for data in imported_data:
            
            updated_id = product.objects.filter(barcode=data[12]).values_list('id', flat=True)
            old_qty = stock.objects.filter(barcode=data[8]).values_list('quantity', flat=True)
            if not updated_id: 
                value = product(data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17])
            else:
                value = product(updated_id[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17])
            try:
                value.save()
            except DatabaseError as e:
                messages.info(request, 'There is data error in the sheet!! ')
                return render(request, 'addproduct.html')

        #storage.used = True
        messages.info(request, 'File Uploaded SuccessFully!')
    return render(request, 'addproduct.html')

