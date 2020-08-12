from django.urls import path
from .views import *

urlpatterns = [
    path('get_category_list', getCategoryList),
    path('search_product', searchProduct),
    path('product_detail/<pk>', getProductDetail),
    path('order_products', orderProducts),
    path('sale_products', saleProducts)
]