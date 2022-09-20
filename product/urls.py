from django.urls import path
from . import views

urlpatterns = [
    path('category/<int:id>/<slug:slug>', views.CATEGORY_PRODUCTS, name='category_products'),
    path('product/<int:id>/<slug:slug>', views.PRODUCT_DETAIL, name='product_detail'),
    path('product/addcomment/<int:id>', views.REVIEW_PRODUCT, name='review_product'),
    path('search/', views.SEARCH, name='search'),



]
