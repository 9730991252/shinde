from django.db import models
from PIL import Image
from sunil.models import *
from product.models import *

from ckeditor.fields import RichTextField

# Create your models here.



class Seller(models.Model):
    shope_name = models.CharField(max_length=100)
    seller_name=models.CharField(max_length=100)
    shop_address = models.CharField(max_length=100)
    seller_mobile=models.IntegerField()
    pin = models.IntegerField()
    status=models.IntegerField(default=1)
    date=models.DateField(auto_now_add=True,null=True)

class Customer (models.Model):
    mobile=models.IntegerField(null=True,blank=True)
    name=models.CharField(max_length=100,null=True,blank=True)
    pin_code = models.IntegerField(null=True,blank=True)    
    house_no=models.CharField(max_length=100,null=True,blank=True)
    post=models.CharField(max_length=100,null=True,blank=True)
    landmark=models.CharField(max_length=100,null=True,blank=True)
    taluka=models.CharField(max_length=100,null=True,blank=True)
    district=models.CharField(max_length=100,null=True,blank=True)
    date=models.DateField(auto_now_add=True,null=True)
    status = models.IntegerField(default=1)




class Category(models.Model):
    category_name = models.CharField(max_length=100)
    status = models.IntegerField(default=1)


class Sub_category(models.Model):
    sub_category_name=models.CharField(max_length=50)
    category=models.ForeignKey(Category,on_delete=models.PROTECT,default=True)
    seller = models.ForeignKey(Seller,on_delete=models.PROTECT,null=True,blank=True)




class Product(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.PROTECT,null=True,blank=True)
    product_name = models.CharField(max_length=100)
    price=models.FloatField(default=0)
    discount = models.IntegerField(null=True,blank=True)
    discription=RichTextField(null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)
    image= models.ImageField(upload_to="images",default="",null=True)
    image_1= models.ImageField(upload_to="images",default="",null=True,blank=True)
    image_2= models.ImageField(upload_to="images",default="",null=True,blank=True)
    image_3= models.ImageField(upload_to="images",default="",null=True,blank=True)

    def save(self, *args,**kwargs):
        super().save(*args,**kwargs)
        image = Image.open(self.image.path)
        output_size = (300,300)
        image.thumbnail(output_size)
        image.save(self.image.path)

        image_1 = Image.open(self.image_1.path)
        output_size = (300,300)
        image_1.thumbnail(output_size)
        image_1.save(self.image_1.path)

        image_2 = Image.open(self.image_2.path)
        output_size = (300,300)
        image_2.thumbnail(output_size)
        image_2.save(self.image_2.path)

        image_3 = Image.open(self.image_3.path)
        output_size = (300,300)
        image_3.thumbnail(output_size)
        image_3.save(self.image_3.path)


class Select_seller_category(models.Model):
    seller = models.ForeignKey(Seller,on_delete=models.PROTECT,null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT,null=True,blank=True)


class Select_sub_category(models.Model):
    product = models.ForeignKey(Product,on_delete=models.PROTECT,null=True,blank=True)
    sub_category = models.ForeignKey(Sub_category,on_delete=models.PROTECT,null=True,blank=True)

