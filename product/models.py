from django.db import models
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.db import models
from ckeditor.fields import RichTextField
from account.models import User
from mptt.models import MPTTModel, TreeForeignKey
from django.forms import ModelForm

# Create your models here.


class Category(MPTTModel):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children',)
    title = models.CharField(max_length=30)
    keywords = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    image=models.ImageField(blank=True,upload_to='images/category/', null=True)
    status=models.CharField(max_length=10, choices=STATUS, default='True')
    slug = models.SlugField(null=False, unique=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class MPTTMeta:
        order_insertion_by = ['title']


    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

    def __str__(self):                           # __str__ method elaborated later in
        full_path = [self.title]                  # post.  use __unicode__ in place of
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' / '.join(full_path[::-1])








class Product(models.Model):
    STATUS = (
        ('True', 'True'),
        ('False', 'False'),
    )


    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    keywords = models.CharField(max_length=255)
    description = RichTextField()
    image=models.ImageField(upload_to='images/product/',null=False)
    price = models.IntegerField()
    discount=models.IntegerField(null=True)
    quantity=models.IntegerField(default=5)
    deal_of_the_day = models.BooleanField()
    new_arrivals = models.BooleanField(default=True)
    best_sellers = models.BooleanField()
    sale_items = models.BooleanField(default=True)
    detail=RichTextField()
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=10,choices=STATUS, default=True)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
        
    def image_tag(self):
        return mark_safe('<img src="{}" weight="50"; height="50"/>'.format(self.image.url))

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name_color = models.CharField(max_length=100)
    code_color = models.CharField(max_length=100)

    def __str__(self):
        return self.name_color



class Images(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank=True)
    image = models.ImageField(blank=True, upload_to='images/image')

    def __str__(self):
        return self.title

    def image_tag(self):
        return mark_safe('<img src="{}" weight="50"; height="50"/>'.format(self.image.url))





class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    ip = models.CharField(max_length=20, blank=True)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['subject','email', 'comment', 'rate']






