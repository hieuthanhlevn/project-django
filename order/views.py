from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from order.models import Order, OrderItem, Wishlist
from product.models import Category, Product
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from account.models import User



@login_required(login_url="/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/login")
def cart_detail(request):
    categorys = Category.objects.all()
    context ={
        'categorys':categorys,
    }
    return render(request, 'cart/cart_detail.html', context)




@login_required(login_url="/login")
def add_to_wishlist(request,slug):
    product = get_object_or_404(Product,slug=slug)
    wished_product,created = Wishlist.objects.get_or_create(wished_product=product, slug = product.slug, user = request.user,)
    return redirect('wishlist')


def WISHLIST(request):
    categorys = Category.objects.all()
    product_wish = Wishlist.objects.all()

    context ={
        'categorys':categorys,
        'product_wish':product_wish,
    }
    return render(request, 'cart/wishlist.html', context)


def deletewishlist(request, id):
    current_user = request.user
    Wishlist.objects.filter(user_id=current_user.id, items=Wishlist.objects.get(id=id)).delete()
    messages.success(request, 'Product Remove From Wishlist...')
    return HttpResponseRedirect('/wishlist')

# def deletewishlist(request, id):
#     current_user = request.user
#     Wishlist.objects.filter(user_id=current_user.id, id=id).delete()
#     messages.success(request, 'Product Remove From Wishlist...')
#     return HttpResponseRedirect('/wishlist')








def CHECK_OUT(request):
    categorys = Category.objects.all()
    context ={
        'categorys':categorys
    }
    return render(request, 'cart/checkout.html', context)


def PLACE_ORDER(request):
    categorys = Category.objects.all()

    if request.method == "POST":
        cart = request.session.get('cart')
        ip = request.META.get('REMOTE_ADDR')
        order = Order()
        order.user = request.user
        order.first_name = request.POST.get('firstname')
        order.last_name = request.POST.get('lastname')
        order.country = request.POST.get('country')
        order.address = request.POST.get('address')
        order.city = request.POST.get('city')
        order.state = request.POST.get('state')
        order.phone = request.POST.get('phone')
        order.email = request.POST.get('email')
        order.amount = request.POST.get('amount')
        order.payment_type = request.POST.get('cash')
        order.ip = ip
        order.order_note = request.POST.get('order_note')
        order.save()

        for i in cart:
            a = (float(cart[i]['price']))
            b = cart[i]['quantity']

            total = a * b

            item = OrderItem(
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
            )
            item.save()
        cart.clear()


    context ={
        'categorys':categorys
    }
    return render(request, 'cart/placeorder.html', context)