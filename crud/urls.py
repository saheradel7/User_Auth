from . import  api
from django.urls import path

urlpatterns = [
    path("product/", api.ProductDetail.as_view() , name="product"),
    path("product/<int:id>", api.ProductInfo.as_view() , name="product"),
    
]
