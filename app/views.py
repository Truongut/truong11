from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import *
import json
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages

# Create your views here.
def register(request):
    form = CreatUserForm()
    if request.method == "POST":
        form = CreatUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'from':form}
    return render(request, 'app/register.html', context)

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request,username =username,password=password)
            if user is not None:
                login(request,user)
                return redirect('home')
            else: messages.info(request,'Tài khoản hoặc mật khẩu sai!')

    context = {}
    return render(request, 'app/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    products = Product.objects.all()
    context= {'products': products}
    return render(request,'app/home.html',context)
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
       
    else:
        items =[] 
        order ={'get_cart_items':0,'get_cart_total':0}   
        cartItems = order['get_cart_items']
    context= {'items':items,'order':order}
    return render(request,'app/cart.html',context)
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer =customer,complete =False)
        items = order.orderitem_set.all()
       
    else:
        items =[] 
        order ={'get_cart_items':0,'get_cart_total':0}   
        cartItems = order['get_cart_items']
    context= {'items':items,'order':order}
    return render(request,'app/checkout.html',context)
def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
        
    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
        
    orderItem.save()
        
    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('added',safe=False)