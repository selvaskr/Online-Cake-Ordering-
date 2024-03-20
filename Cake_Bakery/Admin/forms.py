from User.models import Cake_Products
from django import forms

class Cake_Products_form(forms.ModelForm):
    class Meta:
        model = Cake_Products
        fields = ['product_img','product_name', 'product_des', 'product_price', 'featured_cake']