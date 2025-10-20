from django.contrib import admin
from .models import Service,Contact

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('service_name', 'slug', 'icon_class', 'short_description')
    prepopulated_fields = {'slug': ('service_name',)}
    search_fields = ('service_name', 'slug', 'short_description')
    list_per_page = 20
    ordering = ('service_name',)




@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name','email','company','service_interested','page_source','created_at')
    list_filter = ('service_interested','created_at')
    search_fields = ('name','email','company','message','page_source')
    fieldsets = (('Contact Info',{'fields':('name','email','company')}),('Service & Source',{'fields':('service_interested','page_source','page_url')}),('Message Details',{'fields':('message','created_at')}))
    ordering = ('-created_at',)
    list_per_page = 25
