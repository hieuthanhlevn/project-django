from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from pages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    path('', include('product.urls')),
    path('', include('order.urls')),
    path('', include('account.urls')),
    path('', include('blog.urls')),

    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
