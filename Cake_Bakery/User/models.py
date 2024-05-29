from django.db import models

class Cake_Products(models.Model):
    product_id=models.AutoField(primary_key=True)
    product_name=models.CharField(max_length=255)
    product_price=models.IntegerField()
    product_des=models.TextField(max_length=500, default='Default Description')
    product_img=models.ImageField(upload_to='product_images/',null=True,blank=True)
    featured_cake=models.BooleanField(default=False)


class Customer(models.Model):
    customer_id=models.AutoField(primary_key=True)
    customer_name=models.CharField(max_length=255)
    customer_email=models.EmailField(max_length=254)
    customer_number=models.IntegerField()
    customer_address=models.TextField()

class order(models.Model):

    STATUS=(
        (0,  ('Cancelled')),
        (1, ('Yet to Deliver')),
        (2, ('Delivered'))
    )

    order_id=models.AutoField(primary_key=True)
    order_date = models.DateTimeField(auto_now_add=True)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    product = models.ManyToManyField(Cake_Products, through='OrderItem')
    status = models.PositiveSmallIntegerField(
      choices=STATUS,
      default=1,
   )
    noofitems=models.IntegerField()
    delivery_date=models.DateField(auto_now_add=True)
    Cost=models.IntegerField()

class OrderItem(models.Model):
    order = models.ForeignKey(order, on_delete=models.CASCADE)
    product = models.ForeignKey(Cake_Products, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    size=models.IntegerField()
    Amount=models.IntegerField()
    