from django.contrib import admin
from .models import (
    MainService,
    SubService,
    SubServiceFeature,
    Pricing,
    FAQ,
    CompanyLogo,
    Testimonial,
)


# -------------------------------
# INLINE ADMIN CLASSES
# -------------------------------
class SubServiceFeatureInline(admin.TabularInline):
    model = SubServiceFeature
    extra = 1
    fields = ("title", "description", "icon", "ranking")
    ordering = ("ranking",)


class PricingInline(admin.TabularInline):
    model = Pricing
    extra = 1
    fields = ("plan_name", "price", "duration", "is_popular", "ranking")
    ordering = ("ranking",)


class FAQInline(admin.TabularInline):
    model = FAQ
    extra = 1
    fields = ("question", "answer")


# -------------------------------
# MAIN SERVICE ADMIN
# -------------------------------
@admin.register(MainService)
class MainServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "ranking", "is_featured", "is_active")
    list_filter = ("is_featured", "is_active")
    search_fields = ("title", "short_description")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("ranking",)
    list_editable = ("ranking", "is_featured", "is_active")


# -------------------------------
# SUB SERVICE ADMIN
# -------------------------------
@admin.register(SubService)
class SubServiceAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "main_service",
        "ranking",
        "is_published",
        "created_at",
    )
    list_filter = ("main_service", "is_published")
    search_fields = ("title", "short_description", "overview")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [SubServiceFeatureInline, PricingInline, FAQInline]
    ordering = ("main_service", "ranking")
    list_editable = ("ranking", "is_published")


# -------------------------------
# SUB SERVICE FEATURE ADMIN
# -------------------------------
@admin.register(SubServiceFeature)
class SubServiceFeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "sub_service", "ranking")
    list_filter = ("sub_service",)
    search_fields = ("title", "description")
    ordering = ("sub_service", "ranking")
    list_editable = ("ranking",)


# -------------------------------
# PRICING ADMIN
# -------------------------------
@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ("plan_name", "sub_service", "price", "duration", "is_popular", "ranking")
    list_filter = ("sub_service", "is_popular")
    search_fields = ("plan_name", "description", "features")
    ordering = ("sub_service", "ranking")
    list_editable = ("ranking", "is_popular")


# -------------------------------
# FAQ ADMIN
# -------------------------------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "sub_service")
    list_filter = ("sub_service",)
    search_fields = ("question", "answer")


# -------------------------------
# COMPANY LOGO ADMIN
# -------------------------------
@admin.register(CompanyLogo)
class CompanyLogoAdmin(admin.ModelAdmin):
    list_display = ("name", "website", "logo_preview")
    search_fields = ("name",)
    readonly_fields = ("logo_preview",)

    def logo_preview(self, obj):
        if obj.logo:
            return f'<img src="{obj.logo.url}" width="80" height="40" style="object-fit:contain;" />'
        return "No Logo"
    logo_preview.allow_tags = True
    logo_preview.short_description = "Preview"



@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'designation',
        'company',
        'main_service',
        'sub_service',
        'show_on_home',
        'is_active',
        'ranking',
        'photo_preview',
        'created_at',
    )
    list_filter = (
        'is_active',
        'show_on_home',
        'main_service',
        'sub_service',
        'created_at',
    )
    search_fields = (
        'name',
        'designation',
        'company',
        'message',
        'main_service__title',
        'sub_service__title',
    )
    list_editable = ('is_active', 'show_on_home', 'ranking')
    ordering = ('ranking',)
    readonly_fields = ('photo_preview', 'created_at')

    fieldsets = (
        ('Service Association', {
            'fields': ('main_service', 'sub_service'),
            'description': 'Attach testimonial to a specific Main or Sub Service (optional).'
        }),
        ('Content', {
            'fields': ('name', 'designation', 'company', 'message', 'photo', 'photo_preview')
        }),
        ('Display Settings', {
            'fields': ('show_on_home', 'is_active', 'ranking')
        }),
        ('Meta', {
            'fields': ('created_at',),
        }),
    )

    def photo_preview(self, obj):
        """Show image thumbnail in admin."""
        if obj.photo:
            return f'<img src="{obj.photo.url}" width="60" height="60" style="object-fit: cover; border-radius: 5px;" />'
        return '(No Image)'
    photo_preview.allow_tags = True
    photo_preview.short_description = 'Photo Preview'