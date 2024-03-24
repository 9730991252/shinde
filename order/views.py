from django.shortcuts import render ,redirect
from django.contrib import messages
from django.http import JsonResponse
from product.models import *
from order.models import *

# Create your views here.
def add_to_cart (request):
    if request.method == "GET":
        #print(pid)
        data=[]
        status=36
        ng=0
        if request.session.has_key('customer_mobile'):
            customer_mobile = request.session['customer_mobile']
            c=Customer.objects.get(mobile=customer_mobile)
            pid=request.GET['pid']
            qty=request.GET['qty']
            cp=Cart.objects.filter(product_id=pid,customer_id=c.id)
            #print(qty)
            chk=len(cp)
            if chk == 0:
                Cart(
                    customer_id=c.id,
                    product_id=pid,
                    qty=qty
                ).save()
                ng=len(Cart.objects.filter(customer_id=c.id))
            elif chk == 1:
                Cart.objects.filter(product_id=pid,customer_id=c.id).delete()
                Cart(
                    customer_id=c.id,
                    product_id=pid,
                    qty=qty,

                ).save()
                ng=len(Cart.objects.filter(customer_id=c.id))
        else:
            status=0
            
        data={
            'status':status,
            'ng':ng
            
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'status':0})

def customer_mobile(request):
    if request.method == "GET":
        status=33
        pid=request.GET['pid']
        qty=request.GET['qty']
        mobile=request.GET['mobile']
        s=Customer.objects.filter(mobile=mobile)
        s=len(s)
        if s == 0:
            Customer(
                mobile=mobile
            ).save()
            request.session['customer_mobile'] = mobile
            cn=Customer.objects.get(mobile=mobile)
            cpn=Cart.objects.filter(product_id=pid,customer_id=cn.id)
            chkn=len(cpn)
            if chkn == 0:
                Cart(
                    customer_id=cn.id,
                    product_id=pid,
                    qty=qty
                ).save()
            elif chkn == 1:
                Cart.objects.filter(product_id=pid,customer_id=cn.id).delete()
                Cart(
                    customer_id=cn.id,
                    product_id=pid,
                    qty=qty
                ).save()
        elif s == 1:
            request.session['customer_mobile'] = mobile
            c=Customer.objects.get(mobile=mobile)
            cp=Cart.objects.filter(product_id=pid,customer_id=c.id)
            chk=len(cp)
            if chk == 0:
                Cart(
                    customer_id=c.id,
                    product_id=pid,
                    qty=qty
                ).save()
            elif chk == 1:
                Cart.objects.filter(product_id=pid,customer_id=c.id).delete()
                Cart(
                    customer_id=c.id,
                    product_id=pid,
                    qty=qty,

                ).save()
        data=[]
        data={
            'status':status,
        }
        return JsonResponse(data)
    else:
        return JsonResponse({'status':33})


def cart(request):
    context={}
    if request.session.has_key('customer_mobile'):
        customer_mobile=request.session['customer_mobile']
        cm=Customer.objects.get(mobile=customer_mobile)
        cp=Cart.objects.filter(customer_id=cm.id)
        if 'Remove' in request.GET:
            cart_id=request.GET.get('cart_id')
            if Cart.objects.filter(id=cart_id).first():
                Cart.objects.get(id=cart_id).delete()
                if len(Cart.objects.filter(customer_id=cm.id)) == 0:
                    return redirect('/')

        if 'Add_address' in request.POST:
            name=request.POST.get('name')
            pin_code=request.POST.get('pin_code')
            house_no=request.POST.get('house_no')
            post=request.POST.get('post')
            taluka=request.POST.get('taluka')
            district=request.POST.get('district')
            landmark=request.POST.get('landmark')
            Customer(
                id=cm.id,
                mobile=cm.mobile,
                date=cm.date,
                name=name,
                pin_code=pin_code,
                house_no=house_no,
                post=post,
                taluka=taluka,
                district=district,
                landmark=landmark,
            ).save()
            total_amount=0
            f=OrderMaster.objects.all().count()
            f+=1
            if cp:
                for c in cp:
                    pid=c.product_id
                    qty=c.qty
                    curent_p=Product.objects.filter(id=pid)
                    if curent_p:
                        for curent_p in curent_p:
                            price=curent_p.price
                            discount=curent_p.discount
                            if discount == None:
                                discount =0
                            sellprice=price - (price * discount / 100)
                            total=sellprice*qty
                            total_amount+= total
            OrderMaster(
                customer_id=cm.id,
                total_amount=total_amount,
                order_filter=f,
            ).save()
            total_amount_d=0
            if cp:
                for cd in cp:
                    pid_d=cd.product_id
                    qty_d=cd.qty
                    curent_p_d=Product.objects.filter(id=pid_d)
                    if curent_p_d:
                        for curent_p_d in curent_p_d:
                            price_d=curent_p_d.price
                            discount_d=curent_p_d.discount
                            if discount_d == None:
                                discount_d=0
                            sellprice_d=price_d - (price_d * discount_d / 100)
                            total_d=sellprice_d*qty_d
                            total_amount_d+= total_d
                            Order_detail(
                                customer_id=cm.id,
                                product_id=pid_d,
                                product_name=curent_p_d.product_name,
                                price=curent_p_d.price,
                                sell_price=sellprice_d,
                                discount=discount_d,
                                qty=qty_d,
                                total_price=total_d,
                                order_filter=f,
                            ).save()
                cp=Cart.objects.filter(customer_id=cm.id).delete()
                return redirect('/')
        context={
            'cp':cp,
            'cm':cm
            }
        return render (request,'cart.html',context)

    else:
        return redirect('/')
    
def pending_order(request):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.filter(admin_mobile=admin_mobile).first()
        context={}
        if a:
            a=Admin.objects.get(admin_mobile=admin_mobile)
            pending_order=OrderMaster.objects.all().order_by('-id')
        context={
            'a':a,
            'pending_order':pending_order
        }
        return render(request,'admin/pending_order.html',context)
    else:
        return render(request,'login.html')
    
def view_pending_order(request,id):
    if request.session.has_key('admin_mobile'):
        admin_mobile = request.session['admin_mobile']
        a=Admin.objects.filter(admin_mobile=admin_mobile).first()
        context={}
        if a:
            a=Admin.objects.get(admin_mobile=admin_mobile)
            pd=Order_detail.objects.filter(order_filter=id)
            if pd:
                for c in pd:
                    cid=c.customer_id
            c=Customer.objects.get(id=cid)
        context={
            'a':a,
            'pd':pd,
            'c':c
        }
        return render(request,'admin/view_pending_order.html',context)
    else:
        return render(request,'login.html')
    


