from django.contrib import admin
from .models import Service,Contact,ServiceDetails, BulletPointServices
from django.contrib import admin
from .models import SubService, SubServiceFeature

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


class BulletPointInline(admin.TabularInline):
    model = BulletPointServices
    extra = 1
    fields = ('order', 'title', 'description')

class ServiceDetailsInline(admin.StackedInline):
    model = ServiceDetails
    can_delete = False
    max_num = 1
    inlines = (BulletPointInline,)  # Not directly supported here; show BulletPoint by registering separately below



# Register ServiceDetails and BulletPoint for direct editing if you prefer
@admin.register(ServiceDetails)
class ServiceDetailsAdmin(admin.ModelAdmin):
    list_display = ('service', 'short_section_title', 'created_at')

@admin.register(BulletPointServices)
class BulletPointAdmin(admin.ModelAdmin):
    list_display = ('title', 'details', 'order')
    list_filter = ('details__service',)
    ordering = ('details', 'order')


class SubServiceFeatureInline(admin.TabularInline):
    model = SubServiceFeature
    extra = 1
    fields = ('text', 'order')

@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent_service', 'color_theme', 'is_active', 'order')
    list_editable = ('is_active', 'order')
    prepopulated_fields = {'slug': ('title',)}
    inlines = (SubServiceFeatureInline,)
