from django.shortcuts import render ,redirect
from django.contrib import messages
from django.http import JsonResponse
from product.models import *
from order.models import *
import math

# Create your views here.
def index(request):
    #Select_seller_category.objects.all().delete()
    #Seller.objects.all().delete()
    #Select_category.objects.all().delete()
    #Order_detail.objects.all().delete()
    #Cart.objects.all().delete()
    #OrderMaster.objects.all().delete()
    #Product.objects.all().delete()
    #Customer.objects.all().delete()
    ng=0
    cm=''
    c=Category.objects.all()
    p=[]
    sub={}
    if 'Search' in request.POST:
        cid=request.POST.get('cid')
        s=Sub_category.objects.filter(category_id=cid)
        if s:
            sub=s
    if 'Select' in request.POST:
        sub_category_id=request.POST.get('sub_category_id')
        s=Select_sub_category.objects.filter(sub_category_id=sub_category_id)
        if s:
            for s in s:
                pi=s.product_id
                d=Product.objects.filter(id=pi)
                p.extend(d)
    if request.session.has_key('customer_mobile'):
        customer_mobile = request.session['customer_mobile']
        cm=Customer.objects.filter(mobile=customer_mobile).first()
        if cm:
            cm=Customer.objects.get(mobile=customer_mobile)
            ng=len(Cart.objects.filter(customer_id=cm.id))
        else:
            del request.session['customer_mobile']
    context=''
    context={
        'c':c,
        'p':p,
        'c':c,
        'ng':ng,
        'cm':cm,
        'sub':sub
    }
    return render (request,'index.html',context)





def filter_product(request):
    if request.method == "GET":
        pr=[]
        sellprice=[]
        sub_category_id=request.GET['sub_category_id']
        sub=Select_sub_category.objects.filter(sub_category_id=sub_category_id)
        if sub:
            for s in sub:
                product_id=s.product_id
                r=Product.objects.values().filter(id=product_id)
                #print(type(r))
                pr.extend(r)     
            return JsonResponse({'status':1,'p':pr,'sellprice':sellprice})
        else:
            return JsonResponse({'status':0})





def product_detail(request,id):
    context={}
    ng=0
    p=Product.objects.get(id=id)
    c=Select_sub_category.objects.filter(product_id=p.id).first()
    if c:
        c=Select_sub_category.objects.filter(sub_category_id=c.sub_category_id)
        if c:
            for c in c:
                product_id=c.product_id
                rp=Product.objects.filter(id=product_id)
    if request.session.has_key('customer_mobile'):
        customer_mobile = request.session['customer_mobile']
        cm=Customer.objects.filter(mobile=customer_mobile).first()
        if cm:
            cm=Customer.objects.get(mobile=customer_mobile)
            ng=len(Cart.objects.filter(customer_id=cm.id))
        else:
            del request.session['customer_mobile']

    context={
        'p':p,
        'rp':rp,
        'ng':ng
    }
    return render(request,'product_detail.html',context)


def login (request):
    if request.session.has_key('seller_mobile'):
        return redirect('seller_dashboard')
    if request.session.has_key('admin_mobile'):
        return redirect('admin_dashboard')
    if request.method == "POST":
        mb=request.POST ['mb']
        pin=request.POST ['pin']
        a= Admin.objects.filter(admin_mobile=mb,pin=pin,status=1)
        if a:
            request.session['admin_mobile'] = request.POST["mb"]
            return redirect('admin_dashboard')
        s= Seller.objects.filter(seller_mobile=mb,pin=pin,status=1)
        if s:
            request.session['seller_mobile'] = request.POST["mb"]
            return redirect('seller_dashboard')
        else:
            messages.success(request,"please insert correct information or call more suport 9730991252")              
    return render(request,'login.html')


def seller_dashboard(request):
    if request.session.has_key('seller_mobile'):
        seller_mobile = request.session['seller_mobile']
        s=Seller.objects.filter(seller_mobile=seller_mobile).first()
        context={}
        if s:
            s=Seller.objects.get(seller_mobile=seller_mobile)
        
        context={
            's':s
        }
        return render(request,'seller/seller_dashboard.html',context)
    else:
        return render(request,'login.html')
    
