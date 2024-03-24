from django import template
import math
register = template.Library()
from product.models import *
from order.models import *

@register.simple_tag
def call_sellprice(price,discount):
    if discount is None or discount is 0:
        return price
    sellprice=price
    sellprice = price - (price * discount / 100)
    return math.floor(sellprice)

@register.simple_tag
def call_current_sellprice(id):
    p=Product.objects.get(id=id)
    if p.discount is None or p.discount is 0:
        p.discount =0
    sellprice = p.price - (p.price * p.discount / 100)
    #print(price)
    return math.floor(sellprice)



@register.simple_tag
def call_current_price(id):
    p=Product.objects.get(id=id)
    return math.floor(p.price)

@register.simple_tag
def call_current_discount(id):
    p=Product.objects.get(id=id)
    if p.discount is None or p.discount is 0:
        return 0
    return math.floor(p.discount)




@register.simple_tag
def call_total_price(id,qty):
    p=Product.objects.get(id=id)
    if p.discount is None or p.discount is 0:
        p.discount=0
    print(p.discount)
    sellprice = p.price - (p.price * p.discount / 100)
    total = sellprice * qty
    return math.floor(total)

@register.simple_tag
def call_total_amount(id):
    c=Cart.objects.filter(customer_id=id)
    total_amount=0
    if c:
        for c in c:
            pid=c.product_id
            qty=c.qty
            p=Product.objects.filter(id=pid)
            if p:
                for p in p:
                    if p.discount is None or p.discount is 0:
                        p.discount=0
                    sellprice = p.price - (p.price * p.discount / 100)
                    total=sellprice*qty
                    total_amount+=total
                    #print(total_amount)
    return math.floor(total_amount)