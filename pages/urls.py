from django.urls import path
from . import views

urlpatterns = [
    path('base', views.base, name='base'),
    path('', views.HOME, name='home'),
    path('about', views.ABOUT, name='about'),
    path('contact', views.CONTACT, name='contact'),
    path('shop', views.SHOP, name='shop'),

    
]
