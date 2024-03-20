from django.shortcuts import render,redirect, get_object_or_404,HttpResponse,get_list_or_404
from User.models import *
from .forms import Cake_Products_form
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.views import View

def adminlogin(request):
    if request.user.is_authenticated and request.user.is_staff:
        print(request.user)
        # If the user is already authenticated and is a staff member, redirect to admin home
        return redirect('adminhome')

    # If the user is not authenticated or is not a staff member, proceed with the login
    return LoginView.as_view(template_name='admin/login.html')(request)

@login_required(login_url='/admin/login/')
def adminhome(request):
    count=0
    feature=0
    orders=order.objects.all()
    products = Cake_Products.objects.all()
    for product in products:
        if(product.featured_cake==True):
            feature+=1
        count+=1
        # print("PRODUCTS : ",product)

    allcounts = [
        order.objects.filter(status=2).count(),
        count,
        feature,
        order.objects.filter(status=1).count(), 
        ]
    # print("ALLCOUNTS : ",allcounts)
    # print("\n\nORDER   :    ",orders)
    orderlist={}
    for ordered in orders:
        if ordered.status==1:
            customerorder={}
            customerdetails=get_object_or_404(Customer, customer_id=ordered.customer_id)
            customerorder['orderid']=ordered.order_id
            customerorder['Name']=customerdetails.customer_name
            customerorder['Number']=customerdetails.customer_number
            customerorder['Delivery']=ordered.delivery_date
            customerorder['Amount']=ordered.amount
            orderlist[customerorder['Number']]=customerorder


    context={
        'count':allcounts,
        'orderlist':orderlist
    }
    return render(request,'Admin/Adminhome.html',context)

@login_required(login_url='/admin/login/')
def adminproducts(request): 

    product=Cake_Products.objects.all()
    return render(request,'Admin/Adminproducts.html',{'products':product})

@login_required(login_url='/admin/login/')
def adminaddproducts(request):
    if request.method=='POST':
        form = Cake_Products_form(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect('adminproducts')
    else:
        form=Cake_Products_form()
    return render(request, 'Admin/AdminAddProducts.html', {'form': form, 'action': 'Add'})

@login_required(login_url='/admin/login/')
def admineditproducts(request,product_id):
    
    product=get_object_or_404(Cake_Products,product_id=product_id)

    if request.method=='POST':
        product.product_name=request.POST.get('product_name')
        product.product_price=request.POST.get('product_price')
        product.featured_cake=request.POST.get('featured_cake')
        product.product_des=request.POST.get('product_des')
        product.product_img=request.FILES.get('product_img')
        product.save()
        return redirect('adminproducts')
    
    return render(request, 'Admin/AdminAddProducts.html', {'Product': product, 'action': 'edit'})


@login_required(login_url='/admin/login/')
def admindeleteproduct(request,product_id):
    product=get_object_or_404(Cake_Products, product_id=product_id)
    product.delete()
    return redirect('adminproducts')

@login_required(login_url='/admin/login/')
def adminproductorders(request):
    orders=order.objects.all()
    print("\n\nORDER   :    ",orders)
    orderlist={}
    for ordered in orders:
        if ordered.status!=1:
            customerorder={}
            customerdetails=get_object_or_404(Customer, customer_id=ordered.customer_id)
            customerorder['id']=ordered.customer_id
            customerorder['Name']=customerdetails.customer_name
            customerorder['Number']=customerdetails.customer_number
            customerorder['Delivery']=ordered.delivery_date
            customerorder['Amount']=ordered.amount
            customerorder['Status']=ordered.get_status_display
            orderlist[customerorder['Number']]=customerorder
    # print("\n\nOrders :  ",orderlist)
    
    for key,lists in orderlist.items():
        
        print("Key : ",key,"\n\n List : ",lists)

    return render(request,'Admin/Adminorder.html',{'orderlist':orderlist})

@login_required(login_url='/admin/login/')
def admincustomerpanel(request,id):
    customerdetails=get_object_or_404(Customer, customer_id=id)
    customerorders=get_list_or_404(order, customer_id=id)
    customerorderlist={}
    i=1
    for  orders in customerorders:
        ordereditem=get_list_or_404(OrderItem, order_id=orders.order_id)
        for  products in ordereditem:
            eachlist={}
            productdetail=get_object_or_404(Cake_Products, product_id=products.product_id)
            eachlist['Productname']=productdetail.product_name
            eachlist['Productprice']=products.Amount
            eachlist['Productsize']=products.size
            eachlist['ProductQuantity']=products.quantity
            eachlist['Delivery']=orders.delivery_date
            eachlist['Status']=orders.get_status_display
            customerorderlist[i]=eachlist
            i+=1

    context={
        'eachcustomer':customerdetails,
        'customerorderlist':customerorderlist
    }
    print(customerdetails)
    print("\n\nCustomer order : ",customerorderlist)

    return render(request,'Admin/Admincustomerpanel.html',context)

@login_required(login_url='/admin/login/')
def deliverorcancel(request,orderid,status):

    # print("ORDER ID : ",orderid,"    STATUS : ",status)
    order.objects.filter(order_id=orderid).update(status=status)

    return redirect('adminhome')

class LogoutView(View):
    def get(self, request):
        # Clear the user's session
        request.session.clear()

        # Redirect to the login page (adjust the 'login' URL name according to your project)
        return redirect('adminlogin')
    



    """
    
        ord=get_list_or_404(OrderItem, order_id=ordered.order_id)
        for products in ord:
            product={}
            productdetail=get_object_or_404(Cake_Products, product_id=products.product_id)
            product['cakename']=productdetail.product_name
            product['Quality']=products.quantity
            product['Size']=products.size
            product['Amount']=products.Amount
            customerorder['product'].append(product)
    """