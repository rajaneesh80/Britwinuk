"""britwin_UK URL Configuration

"""
from django.contrib import admin
from django.urls import include, path
from stockapp import views

urlpatterns = [
#	path( 'stockapp', include('stockapp.urls')),
	path('', include('stockapp.urls')),
#    path('stockapp/', include(('stockapp.urls','stockapp'), namespace='stockapp')),
    path('admin/', admin.site.urls),
]