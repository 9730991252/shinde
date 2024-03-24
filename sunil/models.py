from django.db import models

# Create your models here.
class Admin (models.Model):
    admin_name = models.CharField(max_length=100)
    address=models.CharField(max_length=100)
    admin_mobile=models.IntegerField(default=True,unique=True)
    pin = models.IntegerField()
    added_date = models.DateTimeField(auto_now_add=True, null=True)
    status = models.IntegerField(default=1)
