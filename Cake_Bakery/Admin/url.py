from django.urls import path
from .import views

urlpatterns=[
    path('login/',views.adminlogin,name='adminlogin'),
    path('', views.adminhome , name='adminhome'),
    path('adminproducts/',views.adminproducts,name='adminproducts'),
    path('adminaddproducts/',views.adminaddproducts,name='adminaddproducts'),
    path('admineditproducts/<int:product_id>/',views.admineditproducts,name='admineditproducts'),
    path('admindeleteproduct/<int:product_id>/',views.admindeleteproduct,name='admindeleteproduct'),
    path('adminproductorders/',views.adminproductorders,name='adminproductorders'),
    path('admincustomerpanel/<int:id>/',views.admincustomerpanel,name='admincustomerpanel'),
    path('deliverorcancel/<int:orderid>/<int:status>/',views.deliverorcancel,name='deliverorcancel'),
    path('logout/', views.LogoutView.as_view(), name='logout')
]