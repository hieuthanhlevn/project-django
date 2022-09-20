from itertools import product
from tkinter.tix import Tree
from django.db import models
from account.models import User
from product.models import Product
from django.utils.safestring import mark_safe
from django.conf import settings


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Preaparing', 'Preaparing'),
        ('OnShipping', 'OnShipping'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=10)
    last_name = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=150)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=20)
    amount = models.FloatField()
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    order_note = models.CharField(blank=True, max_length=500)
    payment_type = models.CharField(max_length=150)
    paid = models.BooleanField(default=False)
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(blank=True, max_length=100)
    create_at=models.DateField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    def user_name(self):
        return self.user.first_name + ' ' + self.user.last_name + ' [' + self.user.username + '] '




class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.CharField(max_length=250)
    image = models.ImageField(upload_to='images/order/', blank=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    total = models.FloatField()

    def __str__(self):
        return self.order.user.username + ' ' + self.product

    def image_tag(self):
        return mark_safe('<img src="{}" weight="50"; height="50"/>'.format(self.image.url))



class Wishlist(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    wished_product = models.ForeignKey(Product,on_delete=models.CASCADE)
    slug = models.CharField(max_length=30,null=True,blank=True)
    added_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.wished_product.title
    
    def username(self):
        return self.user.username