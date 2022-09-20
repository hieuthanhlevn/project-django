from django.urls import path
from . import views

urlpatterns = [
    path('blog/', views.BLOG, name='blog'),
    path('blog/<int:id>/<slug:slug>', views.BLOG_DETAIL, name='blog_detail'),


]
