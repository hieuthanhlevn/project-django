from django.contrib import admin
from order.models import Order, OrderItem, Wishlist

class OrderProductTabularInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderProductTabularInline]
    list_display = ['user_name','email', 'amount', 'payment_type' ,'status', 'paid', 'create_at']
    list_editable = ('status',)
    list_filter = ['status', 'paid']

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product','image_tag', 'quantity', 'price', 'total']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('username', 'wished_product')
    list_display_links = ('wished_product',)

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

admin.site.register(Wishlist, WishlistAdmin)