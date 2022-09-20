
from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
from . models import Category, Product, Images, Comment, Variation
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter  = ['status']

class CategoryAdmin2(DraggableMPTTAdmin):
    mptt_indent_field = "title"
    list_display = ('tree_actions', 'indented_title','related_products_count', 'related_products_cumulative_count')
    list_display_links = ('indented_title',)
    prepopulated_fields = {'slug': ('title',)}
    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Add cumulative product count
        qs = Category.objects.add_related_count(
                qs,
                Product,
                'category',
                'products_cumulative_count',
                cumulative=True)

        # Add non cumulative product count
        qs = Category.objects.add_related_count(qs,
                 Product,
                 'category',
                 'products_count',
                 cumulative=False)
        return qs

    def related_products_count(self, instance):
        return instance.products_count
    related_products_count.short_description = 'Related products (for this specific category)'

    def related_products_cumulative_count(self, instance):
        return instance.products_cumulative_count
    related_products_cumulative_count.short_description = 'Related products (in tree)'




class ProductImageInline(admin.TabularInline):
    model = Images
    readonly_fields = ('id',)
    extra = 5



class ProductAdmin(admin.ModelAdmin):
    list_display = ['image_tag', 'title','price', 'discount', 'category', 'status', 'deal_of_the_day', 'new_arrivals', 'best_sellers', 'sale_items']
    list_editable = ('status','deal_of_the_day', 'new_arrivals', 'best_sellers', 'sale_items')
    search_fields = ('title', 'category')
    list_display_links =['image_tag', 'title',]
    readonly_fields = ('image_tag',)
    inlines = [ProductImageInline,]
    prepopulated_fields = {'slug': ('title',)}


class ImagesAdmin(admin.ModelAdmin):
    list_display = ['product', 'title', 'image_tag']

class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'name_color', 'code_color')

admin.site.register(Images, ImagesAdmin)
admin.site.register(Category, CategoryAdmin2)
admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)

admin.site.register(Variation, VariationAdmin)