from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Category, Product, Images, Comment, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def PRODUCT_DETAIL(request, id, slug):
    categorys = Category.objects.all()
    product = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    context ={
        'categorys':categorys,
        'product':product,
        'images':images
    }
    return  render(request, 'products/product_details.html', context)





def CATEGORY_PRODUCTS(request, id, slug):
    categorys = Category.objects.all()
    products = Product.objects.filter(category_id=id,)

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    products_count = products.count()

    context ={
        'categorys':categorys,
        'products':paged_products,
        'products_count':products_count
    }
    return render(request, 'products/search_products.html', context)



def SEARCH(request):
    categorys = Category.objects.all()
    query = request.GET.get('query')
    products = Product.objects.filter(description__contains=query, title__contains=query).order_by('-id')

    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    paged_products = paginator.get_page(page)

    products_count = products.count()

    context ={
        'categorys':categorys,
        'products':paged_products,
        'products_count':products_count,

    }
    return render(request, 'products/search_products.html', context)




def REVIEW_PRODUCT(request, id):
    url = request.META.get('HTTP_REFERER')  # get last url
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            data = Comment()
            data.subject = form.cleaned_data['subject']
            data.email = form.cleaned_data['email']
            data.comment = form.cleaned_data['comment']
            data.rate = form.cleaned_data['rate']
            data.ip = request.META.get('REMOTE_ADDR')
            data.product_id=id
            current_user= request.user
            data.user_id=current_user.id
            data.save()
            messages.success(request, "Your review has ben sent. Thank you for your interest.")
    return HttpResponseRedirect(url)






