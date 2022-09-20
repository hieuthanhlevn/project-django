from http.client import HTTPResponse
from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from product.models import Category, Product
from . models import ContactMessage, Slider
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from blog.models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger







def  base(request):
    categorys = Category.objects.all()
    context = {
        'categorys':categorys,
    }
    return render(request, 'base.html', context)




def  HOME(request):
    categorys = Category.objects.all()
    products = Product.objects.all()
    sliders = Slider.objects.filter(status='Active').order_by('-id')[:3]

    product_deal_of = Product.objects.all().filter(deal_of_the_day=True, status=True).order_by('-id')
    product_new_arrivals = Product.objects.filter(new_arrivals=True, status=True).order_by('-id')[:8]
    product_best_sellers = Product.objects.filter(best_sellers=True, status=True).order_by('-id')[:8]
    product_sale_items = Product.objects.filter(sale_items=True, status=True).order_by('-id')[:8]

    posts = Post.objects.filter(status=1).order_by('-id')[:3]

    context = {
        'categorys':categorys,
        'sliders':sliders,
        'products':products,
        'product_deal_of':product_deal_of,
        'product_new_arrivals':product_new_arrivals,
        'product_best_sellers':product_best_sellers,
        'product_sale_items':product_sale_items,
        'posts':posts
    }
    return render(request, 'pages/home.html', context)







def  ABOUT(request):
    categorys = Category.objects.all()
    context = {
        'categorys':categorys,

    }
    return render(request, 'pages/about_us.html', context)





def  CONTACT(request):
    categorys = Category.objects.all()

    if request.method=="POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        phoneuser = request.POST.get('phone')
        message = request.POST.get('message')
        client_ip = request.META['REMOTE_ADDR']
        ct = ContactMessage(name=name, email=email, ip=client_ip,phoneuser=phoneuser, subject=subject, message=message)

        # Thong bao den email
        subject = subject
        message = message
        email_from = settings.EMAIL_HOST_USER
        try:
            send_mail(subject, message, email_from, ['djangohieule@gmail.com'])
            ct.save()
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
            return HttpResponseRedirect('/contact')
        except:
            return redirect('home')


    context = {
        'categorys':categorys,

    }
    return render(request, 'pages/contact_us.html', context)



def SHOP(request):
    categorys = Category.objects.all()
    products = Product.objects.all().order_by('-id')

    paginator = Paginator(products, 8)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    product_count = products.count()

    context = {
        'categorys':categorys,
        'products':paged_products,
        'product_count':product_count
    }
    return render(request, 'pages/shop.html', context)


