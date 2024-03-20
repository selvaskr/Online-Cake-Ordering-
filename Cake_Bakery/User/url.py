from django.urls import path
from .import views

urlpatterns=[
    path('',views.home,name='home'),
    path('products/',views.products,name='products'),
    path('productdetail/<int:product_id>/',views.productdetail,name='productdetail'),
    path('addtocart/<int:product_id>/',views.add_to_cart,name='addtocart'),
    path('viewcart/',views.viewcart,name='viewcart'),
    path('deletecartproduct/<str:key>/',views.deletecartproduct,name='deletecartproduct'),
    path('orderproducts/',views.orderproducts,name='orderproducts'),
    path('sample/',views.sample,name='sample')
]