from django.db import models
from product.models import*

# Create your Order models here.







class Cart(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,default=True)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    qty = models.IntegerField(default=1)    
    date=models.DateField(auto_now_add=True,null=True)


STATUS_CHOICES = (
  ('Accepted','Accepted'),
  ('Packed','Packed'),
  ('On The Way','On The Way'),
  ('Delivered','Delivered'),
  ('Cancel','Cancel'),
  ('Pending','Pending'),

)


INSTOCK_OUTSTOCK_CHOICE=(
    ('1','in stock'),
    ('0','out of stock')
)


class OrderMaster(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,default=True)
    status = models.CharField(choices=STATUS_CHOICES,default='Pending',max_length=50)
    total_amount=models.FloatField(default=0,null=True)
    order_filter=models.IntegerField(default=True)
    date=models.DateField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)

class Order_detail(models.Model):
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT,default=True)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,default=True)
    product_name = models.CharField(max_length=100)
    price=models.FloatField(default=0)
    sell_price=models.FloatField(default=0)
    discount = models.IntegerField(null=True,blank=True)
    qty = models.IntegerField(default=1) 
    total_price=models.FloatField(default=0,null=True)
    order_filter=models.IntegerField(default=True)
    stock_status = models.IntegerField(choices=INSTOCK_OUTSTOCK_CHOICE,default=1)
    date=models.DateField(auto_now_add=True,null=True)
    ordered_date = models.DateTimeField(auto_now_add=True,null=True)

