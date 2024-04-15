from django.shortcuts import render ,redirect
from django.contrib import messages
from django.http import JsonResponse
from product.models import *

# Create your views here.


def add_seller(request):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.filter(admin_mobile=admin_mobile).first()
        if a:
            a=Admin.objects.get(admin_mobile=admin_mobile)
            s=Seller.objects.all()
        context={
            'a':a, 
            's':s
        }
        if request.method == "POST":
            if "Add" in request.POST:
                shope_name=request.POST.get('shope_name')
                seller_name=request.POST.get('seller_name')
                shop_address=request.POST.get('shop_address')
                seller_mobile=request.POST.get('seller_mobile')
                pin=request.POST.get('pin')
                if Seller.objects.filter(seller_mobile=seller_mobile).exists():
                    messages.success(request,"Seller Allready Exists")
                else:

                    Seller(
                        shope_name=shope_name,
                        seller_name=seller_name,
                        shop_address=shop_address,
                        seller_mobile=seller_mobile,
                        pin=pin,
                    ).save()
                    messages.success(request,"Category Added Succesfully")
                    return redirect ('/product/add_seller/')
            elif "Edit" in request.POST:
                seller_id=request.POST.get('seller_id')
                shope_name=request.POST.get('shope_name')
                seller_name=request.POST.get('seller_name')
                shop_address=request.POST.get('shop_address')
                seller_mobile=request.POST.get('seller_mobile')
                pin=request.POST.get('pin')
                Seller(
                    id=seller_id,
                    shope_name=shope_name,
                    seller_name=seller_name,
                    shop_address=shop_address,
                    seller_mobile=seller_mobile,
                    pin=pin,
                ).save()
                messages.success(request,"Category Edit Successfully")
            elif "Active" in request.POST:
                id=request.POST.get('id')
                ac=Seller.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                ac=Seller.objects.get(id=id)
                ac.status='1'
                ac.save()            
        return render(request,'add_seller.html',context=context)
    else:
        return redirect('/login/')





def shop_category(request):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.get(admin_mobile=admin_mobile)
        dc=Category.objects.filter().all()
        context={
            'dc':dc,
            'a':a,       
        }
        if request.method == "POST":
            if "Add" in request.POST:
                name=request.POST.get('name')
                admin_id = request.POST.get('admin_id')
                Category.objects.create(
                    category_name=name,
                )
                messages.success(request,"Category Added Succesfully")
                return redirect ('/product/category/')
            elif "Edit" in request.POST:
                name=request.POST.get('name')
                id=request.POST.get('id')
                edit_category=Category.objects.get(id=id)
                edit_category.category_name=name
                edit_category.save()
                messages.success(request,"Category Edit Successfully")
            elif "Delete" in request.POST:
                id=request.POST.get('id')
                Category.objects.get(id=id).delete()
                messages.success(request,"Category Delete Successfully")
            elif "Active" in request.POST:
                id=request.POST.get('id')
                ac=Category.objects.get(id=id)
                ac.status='0'
                ac.save()
            elif "Deactive" in request.POST:
                id=request.POST.get('id')
                ac=Category.objects.get(id=id)
                ac.status='1'
                ac.save()            
        return render(request,'shop_category.html',context=context)
    else:
        return redirect('/login/')



def seller_select_category(request,id):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.filter(admin_mobile=admin_mobile).first()
        c=Category.objects.all()
        context={}
        if a:
            a=Admin.objects.get(admin_mobile=admin_mobile)
            s=Seller.objects.get(id=id)
        if "Select" in request.POST:
            cid=request.POST.get('category_id')
            s=Select_seller_category.objects.filter(seller_id=id,category_id=cid)
            s=len(s)
            if s == 0 :
                Select_seller_category(
                    seller_id=id,
                    category_id=cid
                ).save()
                return redirect(f'/product/seller_select_category/{id}')
            elif s == 1:
                Select_seller_category.objects.filter(seller_id=id,category_id=cid).delete()
                return redirect(f'/product/seller_select_category/{id}')

        context={
            'a':a,
            's':s,
            'c':c
        }
        return render(request,'seller_select_category.html',context)
    else:
        return render(request,'login.html')
    


def select_seller_cat (request):
    if request.method == "GET":
        seller_id=request.GET['seller_id']
        sl=Select_seller_category.objects.values().filter(seller_id=seller_id)
        sl=list(sl)
        return JsonResponse({'status':1,'sl':sl})
    else:
        return JsonResponse({'status':0})


    


def product_select_category(request,id):
    if request.session.has_key('seller_mobile'):
        seller_mobile = request.session['seller_mobile']
        s=Seller.objects.filter(seller_mobile=seller_mobile).first()
        context={}
        sub_c={}
        c=[]
        if s:
            s=Seller.objects.get(seller_mobile=seller_mobile)
            p=Product.objects.get(id=id)
            st=Select_seller_category.objects.filter(seller_id=s.id)
            if st:
                for st in st:
                    category_id=st.category_id
                    k=Category.objects.filter(id=category_id).first()
                    sub_c=Sub_category.objects.filter(category_id=category_id)
                    c.append(k)
        if "Search" in request.POST:
            category_id=request.POST.get('category_id')
            sub_c=Sub_category.objects.filter(category_id=category_id)
        elif "Add" in request.POST:
            name=request.POST.get('sub_category_name')
            main_cat_id=request.POST.get('main_cat_id')
            Sub_category(
                sub_category_name=name,
                category_id=main_cat_id,
                seller_id=s.id,
            ).save()
            return redirect(f'/product/product_select_category/{id}')
        elif "Select" in request.POST:
            sub_category_id=request.POST.get('sub_category_id')
            s=Select_sub_category.objects.filter(product_id=id,sub_category_id=sub_category_id)
            s=len(s)
            if s == 0 :
                Select_sub_category(
                    product_id=id,
                    sub_category_id=sub_category_id
                ).save()
            elif s == 1:
                Select_sub_category.objects.filter(product_id=id,sub_category_id=sub_category_id).delete()

        context={
            's':s,
            'p':p,
            'c':c,
            'sub_c':sub_c
        }
        return render(request,'seller/product_select_category.html',context)
    else:
        return render(request,'login.html')
    




    
def seller_product(request):
    if request.session.has_key('seller_mobile'):
        context={}
        seller_mobile = request.session['seller_mobile']
        s=Seller.objects.filter(seller_mobile=seller_mobile).first()
        if s:
            s=Seller.objects.get(seller_mobile=seller_mobile)
            p=Product.objects.filter(seller_id=s.id)

        if "Active" in request.POST:
            id=request.POST.get('id')
            ac=Product.objects.get(id=id)
            ac.status='0'
            ac.save()
        elif "Deactive" in request.POST:
            id=request.POST.get('id')
            ac=Product.objects.get(id=id)
            ac.status='1'
            ac.save()  
        context={
            's':s,
            'p':p
        }
        return render(request, 'seller/seller_product.html',context)
    else:
        return render(request,'login.html')

def add_product(request):
    if request.session.has_key('seller_mobile'):
        seller_mobile = request.session['seller_mobile']
        s=Seller.objects.filter(seller_mobile=seller_mobile).first()
        if s:
            s=Seller.objects.get(seller_mobile=seller_mobile)
        if request.method == "POST":
            product_name=request.POST.get('product_name')
            price=request.POST.get('price')
            discount=request.POST.get('discount')
            if discount == "":
                discount = None
            image = request.FILES.get("image")
            image_1 = request.FILES.get("image_1")
            image_2 = request.FILES.get("image_2")
            image_3 = request.FILES.get("image_3")
            discription=request.POST.get('editordata')
            Product(
                product_name=product_name,
                price=price,
                seller_id=s.id,
                discount=discount,
                image=image,
                image_1=image_1,
                image_2=image_2,
                image_3=image_3,
                discription=discription
            ).save()
            return redirect('/product/seller_product/')
        return render(request, 'seller/add_product.html')
    else:
        return render(request,'login.html')

def edit_product(request,id):
    if request.session.has_key('seller_mobile'):
        seller_mobile = request.session['seller_mobile']
        s=Seller.objects.filter(seller_mobile=seller_mobile).first()
        if s:
            s=Seller.objects.get(seller_mobile=seller_mobile)
            p=Product.objects.get(id=id)
            if request.method == "POST":
                product_name=request.POST.get('product_name')
                price=request.POST.get('price')
                discount=request.POST.get('discount')
                if discount == "":
                    discount = None
                discription=request.POST.get('editordata')
                image = request.FILES.get("image")
                if image == None:
                    i=Product.objects.get(id=id)
                    image=i.image
                    #print(image)
                image_1 = request.FILES.get("image_1")
                if image_1 == None:
                    i=Product.objects.get(id=id)
                    image_1=i.image_1
                    #print(image_1)
                image_2 = request.FILES.get("image_2")
                if image_2 == None:
                    i=Product.objects.get(id=id)
                    image_2=i.image_2
                    #print(image)
                image_3 = request.FILES.get("image_3")
                if image_3 == None:
                    i=Product.objects.get(id=id)
                    image_3=i.image_3
                    #print(image)
                Product(
                    product_name=product_name,
                    price=price,
                    seller_id=s.id,
                    discount=discount,
                    id=id,
                    image=image,
                    image_1=image_1,
                    image_2=image_2,
                    image_3=image_3,
                    discription=discription
                ).save()
                messages.success(request,"Product Edit Succesfully")
                return redirect('/product/seller_product/')    
            return render(request, 'seller/edit_product.html',{'p':p})
        else:
            return render(request,'login.html')

def product(request):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.get(admin_mobile=admin_mobile)
        dc=Category.objects.filter().all()
        d=Product.objects.filter().all().order_by('id')
        context={
            'c':dc,
            'a':a,
            'd':d 
            }      
        
        if "Delete" in request.POST:
            product_id=request.POST.get('product_id')

            if Product.objects.filter(id=product_id).first():
                Product.objects.get(id=product_id).delete()
            messages.success(request,"Product Delete Successfully")
        elif "Active" in request.POST:
            id=request.POST.get('id')
            ac=Product.objects.get(id=id)
            ac.status='0'
            ac.save()
        elif "Deactive" in request.POST:
            id=request.POST.get('id')
            ac=Product.objects.get(id=id)
            ac.status='1'
            ac.save()            
        return render(request,'product.html',context=context)
    else:
        return redirect('/login/')
    

def select_prd_cat (request):
    if request.method == "GET":
        pid=request.GET['pid']
        sl=Select_sub_category.objects.values().filter(product_id=pid)
        sl=list(sl)
        return JsonResponse({'status':1,'sl':sl})
    else:
        return JsonResponse({'status':0})


    
