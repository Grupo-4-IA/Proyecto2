from django.urls import re_path
from webScraping import views 

urlpatterns = [ 
    re_path('prueba', views.prueba),
    re_path('inicio', views.returnProducts),
]