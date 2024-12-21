# from http.client import HTTPResponse
from django.http import JsonResponse
from django.shortcuts import redirect, render
from web.forms import CustomUserForm
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
import json

def home(request):
    products=Product.objects.filter(trending=1)
    return render(request,"/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/web/index.html", {'products': products})


def favviewpage(request):
   if request.user.is_authenticated:
      fav=Favorite.objects.filter(user=request.user)
      return render(request,"/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/web/fav.html", {'fav': fav})
   else:
       return redirect('/')

def remove_fav(request,fid):
   item=Favorite.objects.get(id=fid)
   item.delete()
   return redirect('/favviewpage')


def cart_page(request):
   if request.user.is_authenticated:
      cart=Cart.objects.filter(user=request.user)
      return render(request,"/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/web/cart.html", {'cart': cart})
   else:
       return redirect('/')

def remove_cart(request,cid):
   cartitem=Cart.objects.get(id=cid)
   cartitem.delete()
   return redirect('/cart')


def fav_page(request):
   if request.headers.get('X-Requested-With')=='XMLHttpRequest':
      if request.user.is_authenticated:
         data=json.load(request)
         product_id=data['pid']
         # print(request.user.id)
         product_status = Product.objects.get(id=product_id)
         if product_status:
          if  Favorite.objects.filter(user=request.user.id,product_id=product_id):
              return JsonResponse({'status':'Product Already in Favorite'},status=200)
          else:
            Favorite.objects.create(user=request.user,product_id=product_id)
            return JsonResponse({'status':'Product Added to Favorite'},status=200)
      
      else:
       return JsonResponse({'status':'Login to Add Favorite'},status=200)
   else:
      return JsonResponse({'status':'Invalid Access'},status=200)
   

def add_to_cart(request):
   if request.headers.get('X-Requested-With')=='XMLHttpRequest':
      if request.user.is_authenticated:
         data=json.load(request)
         product_qty=data['product_qty']
         product_id=data['pid']
         # print(request.user.id)
         product_status = Product.objects.get(id=product_id)
         if product_status:
          if Cart.objects.filter(user=request.user.id,product_id=product_id):
              return JsonResponse({'status':'Product Already in Cart'},status=200)
          else:
             if product_status.quantity>=product_qty:
               Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
               return JsonResponse({'status':'Product Added to Cart'},status=200)
             else:
                return JsonResponse({'status':'Out of Stock'},status=200)
      else:
       return JsonResponse({'status':'Login to Add Cart'},status=200)
   else:
      return JsonResponse({'status':'Invalid Access'},status=200)
   

def logout_page(request):
   if request.user.is_authenticated:
    logout(request)
    messages.success(request,"Successfully logout")
    return redirect('/')

def login_page(request):
   if request.user.is_authenticated:
      return redirect('/')
   else:
       if request.method=='POST':
         name=request.POST.get('username')
         pwd=request.POST.get('password')
         user=authenticate(request,username=name,password=pwd)
         if user is not None:
           login(request,user)
           messages.success(request,"Successfully login")
           return redirect('/')
         else:
           messages.error(request,"Invalid Username or Password")
           return redirect("/login")
       return render(request,'/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/web/login.html')

def register(request):
    form = CustomUserForm()
    if request.method=='POST':
       form=CustomUserForm(request.POST)
       if form.is_valid():
          form.save()
          messages.success(request,"Registration Success You can Login Now...!")
          return redirect('/login')
    return render(request,"/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/web/register.html",{'form':form})

def collections(request):
    category = Category.objects.filter(status=0)  
    return render(request,'/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/collections.html', {'category': category})

def collectionsview(request,name):
   if Category.objects.filter(name=name,status=0):
    products=Product.objects.filter(Category__name=name)
    return render(request, '/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/products/index.html', {'products': products,"Category__name":name})
   else:
      messages.warning(request,"No Search Category Found")
      return redirect('collections')
   

def product_details(request,name,pname):
   if Category.objects.filter(name=name,status=0):
      if Product.objects.filter(name=pname,status=0):
         products=Product.objects.filter(name=pname,status=0).first()
         return render(request, '/Users/nambivelnathan/Desktop/backendecommerce/pro/web/template/products/product_details.html', {'products': products})
      else:
         messages.warning(request,"No Search Category Found")
         return redirect('collections')
      
   else:
      messages.warning(request,"No Search Category Found")
      return redirect('collections')