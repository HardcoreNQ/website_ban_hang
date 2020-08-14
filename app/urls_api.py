from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views 

urlpatterns = [
    path('token', jwt_views.TokenObtainPairView.as_view()),
    path('token/refresh', jwt_views.TokenRefreshView.as_view()),
    path('signup', signup),
    path('get_category_list', getCategoryList),
    path('search_product', searchProduct),
    path('product_detail/<pk>', getProductDetail),
    path('order_products', orderProducts),
    path('sale_products', saleProducts)
]