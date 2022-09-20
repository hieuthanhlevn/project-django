from django.shortcuts import render
from product.models import Category
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def BLOG(request):
    categorys = Category.objects.all()
    posts = Post.objects.filter(status='1').order_by('-id')

    context ={
        'categorys':categorys,
        'posts':posts
    }
    return  render(request, 'blog/blog.html', context)





def BLOG_DETAIL(request, id, slug):
    categorys = Category.objects.all()
    post = Post.objects.get(pk=id)

    context ={
        'categorys':categorys,
        'post':post
    }
    return  render(request, 'blog/blog-details.html', context)