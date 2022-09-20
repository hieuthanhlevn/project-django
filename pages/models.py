from django.db import models
from ckeditor.fields import RichTextField
from django.db import models
from django.forms import ModelForm, TextInput, Textarea
from django.utils.safestring import mark_safe





class ContactMessage(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Read', 'Read'),
        ('Closed', 'Closed'),
    )
    name= models.CharField(blank=True,max_length=20)
    email= models.CharField(blank=True,max_length=50)
    subject= models.CharField(blank=True,max_length=50)
    phoneuser= models.CharField(max_length=20)
    message= models.TextField(blank=True,max_length=255)
    status=models.CharField(max_length=10,choices=STATUS,default='New')
    ip = models.CharField(blank=True, max_length=20)
    note = models.CharField(blank=True, max_length=100)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Slider(models.Model):
    STATUS = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    topic = models.CharField(blank=True,max_length=100)
    name = models.CharField(blank=True,max_length=100)
    image = models.ImageField(blank=True, upload_to='images/slider')
    status=models.CharField(max_length=10,choices=STATUS, default='Active')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
    def image_tag(self):
        return mark_safe('<img src="{}" weight="50"; height="50"/>'.format(self.image.url))



