from django.urls import path
from order import views

urlpatterns = [
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    path('cart/checkout/',views.CHECK_OUT,name='checkout'),
    path('cart/checkout/placeorder/',views.PLACE_ORDER, name='place_order'),
    path('wishlist/<slug:slug>', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist', views.WISHLIST, name='wishlist'),

    path('wishlist_item/deleteproduct/<int:id>', views.deletewishlist, name="deletewishlist"),

]
