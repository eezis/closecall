from django.contrib import admin
from .models import UserInput, Product

# Register your models here.

admin.site.register(UserInput)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'is_featured', 'is_active', 'order']
    list_filter = ['category', 'is_featured', 'is_active']
    search_fields = ['name', 'description', 'amazon_asin']
    list_editable = ['is_featured', 'is_active', 'order']
    ordering = ['order', 'name']
    
    fieldsets = (
        ('Product Information', {
            'fields': ('name', 'description', 'category')
        }),
        ('Amazon Details', {
            'fields': ('amazon_asin', 'amazon_url')
        }),
        ('Display Settings', {
            'fields': ('price', 'image_url', 'is_featured', 'is_active', 'order')
        }),
    )