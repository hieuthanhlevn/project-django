from django.contrib import admin
from . models import ContactMessage, Slider

# Register your models here.


class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title', 'update_at','status']


class ContactAdmin(admin.ModelAdmin):
    list_display = ['name','subject','phoneuser', 'message','status', 'note', 'update_at']
    search_fields = ['name', 'status']
    list_filter = ['status']

class SliderAdmin(admin.ModelAdmin):
    list_display = ['topic','name','image_tag','status', 'update_at']
    readonly_fields = ['image_tag']


admin.site.register(ContactMessage, ContactAdmin)
admin.site.register(Slider, SliderAdmin)