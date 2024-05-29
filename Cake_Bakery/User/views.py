from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from .models import *

# Create your views here.
def home(request):
    products=Cake_Products.objects.all()
    return render(request,'home.html',{'products':products})

def products(request):
    products=Cake_Products.objects.all()
    return render(request,'Products.html',{'products':products})

def productdetail(request,product_id):
    product=get_object_or_404(Cake_Products,product_id=product_id)
    return render(request,'productdetail.html',{'product':product})

def add_to_cart(request,product_id):
    product = get_object_or_404(Cake_Products,product_id=product_id)
    if request.method=='POST':
        size=request.POST.get('size')
        quantity=request.POST.get('quantity')
        #print(size,quantity)

    cart=request.session.get('cart',{})
    if not isinstance(cart, dict):
        cart = {}
    item=cart.get(product_id,{'quantity': 0, 'size': None, 'price': 0})
    item['quantity']=int(quantity)
    item['size']=size
    item['price']=int(quantity)*product.product_price
    cart[product_id]=item
    # print("\n\nItem : ",item)
    # print("\n\n\nTYPE OF CART : ",type(cart),"\n","TYPE OF ITEM : ",type(item),"\n\n\n")
    request.session['cart']=cart
    request.session.save()
    # print(request.session['cart'])
    return redirect(products)


def viewcart(request):

    merged_cart={}
    cart = request.session.get('cart', {})
    #print("\n\n",'Cart in view_cart :'," \n", cart,"\n\n")
    # Iterate through the items in the cart

    # print(cart)
    amount=0
    for product_id_str, item in cart.items():
        
        product_id = int(product_id_str)
        product = get_object_or_404(Cake_Products, product_id=product_id)

        # Merge the cart item with additional product information
        merged_cart[product_id] = {
            'quantity': item['quantity'],
            'size':item['size'],
            'imgpath':product.product_img.url,
            'name': product.product_name,
            'price':item['price']
        } 
        amount+=item['price']
    # print("\nMerged Cart with Product Information:\n", merged_cart, "\n","Amount : ",amount)

    request.session['cart']=merged_cart
    # for product_id, item in merged_cart.items():
    #     print(f"Product ID: {product_id}, Quantity: {item['quantity']}")
    #     print("Product Information:", item['product'])
    context = {
        'merge':merged_cart,
        'amount':amount
    }
    if cart:
         return render(request,'viewcart.html',context)
    else:
        return redirect(products)
    
def deletecartproduct(request,key):
    cart = request.session.get('cart', {})
    del cart[str(key)]
    request.session['cart']=cart
    return redirect(viewcart)

def orderproducts(request):

    if request.method=='POST':
        mobile=request.POST['mobile']
        name=request.POST['name']
        email=request.POST['email']
        address=request.POST['address']
        customer,created=Customer.objects.get_or_create(customer_number=mobile , defaults={
            'customer_name':name,
            'customer_email':email,
            'customer_number':mobile,
            'customer_address':address
        })
        cart=request.session.get('cart', {})
        ordered=order.objects.create(customer=customer)
        amount=0
        no_of_items=0
        for product_id,item in cart.items():
            product= get_object_or_404(Cake_Products, product_id=product_id)
            OrderItem.objects.create(
                order=ordered,
                product=product,
                quantity=item['quantity'],
                size=item['size'],
                Amount=item['price']
            )
            no_of_items+=1
            print("ITEM : ",item)
            amount=amount+item['price']

        delivery_date=request.POST['delivery']
        ordered.delivery_date=delivery_date
        ordered.Cost=amount
        ordered.noofitems=no_of_items 
        ordered.save()

        print("\n\nUser ordered : ",ordered.Cost)
        print("\n\nUser ordered : ",ordered.delivery_date)
        request.session['cart'] = []
        return redirect(home)
    return render(request,'order.html')

def sample(request):
    return render(request,'sample.html')