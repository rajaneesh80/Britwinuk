from django.urls import path
#from .views import stockListView

from .import views

urlpatterns = [
	path('', views.home, name='home'),
    #path('', views.index, name='index'),
    path('add_stock/', views.add_stock, name='addstock'),
    path('add_product/', views.add_product, name='addproduct'),
    path('del_stock/', views.del_stock, name='delstock'),
    path('view_stock/', views.StockListView.as_view(), name='viewstock'),
	path('view_product/', views.ProductListView.as_view(), name='viewproduct'),
	#path('about/', views.about, name='about'),
    path('export/', views.export_data, name='exportdata'),
#    path('stockapp/index.html', stockListView.as_view()),
]