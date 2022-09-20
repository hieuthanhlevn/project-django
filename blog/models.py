from django.db import models
from account.models import User
from ckeditor.fields import RichTextField
from django.urls import reverse

STATUS = (
    (0, "Draft"),
    (1, "Published"),
)

class Post(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug  = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = 'blog')
    content = RichTextField()
    status = models.IntegerField(choices=STATUS, default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})