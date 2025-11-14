from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import Truncator
from .models import UserInput, Product, SpamTrapEntry


@admin.register(UserInput)
class UserInputAdmin(admin.ModelAdmin):
    list_display = ['subject', 'first', 'last', 'email', 'message_preview', 'linked_user', 'created']
    list_filter = ['created']
    search_fields = ['subject', 'first', 'last', 'email', 'message']
    readonly_fields = ['created', 'linked_user_detail']
    date_hierarchy = 'created'

    fieldsets = (
        ('Contact Information', {
            'fields': ('first', 'last', 'email', 'linked_user_detail')
        }),
        ('Message', {
            'fields': ('subject', 'message')
        }),
        ('Metadata', {
            'fields': ('created',)
        }),
    )

    def message_preview(self, obj):
        """Show first 100 characters of the message"""
        if obj.message:
            return Truncator(obj.message).chars(100)
        return '-'
    message_preview.short_description = 'Message Preview'

    def linked_user(self, obj):
        """Show link to user profile if email matches a registered user"""
        if obj.email:
            try:
                user = User.objects.get(email=obj.email)
                url = reverse('admin:auth_user_change', args=[user.id])
                return format_html('<a href="{}">View User</a>', url)
            except User.DoesNotExist:
                return '-'
            except User.MultipleObjectsReturned:
                return 'Multiple users'
        return '-'
    linked_user.short_description = 'Registered User'

    def linked_user_detail(self, obj):
        """Detailed link to user profile for the detail view"""
        if obj.email:
            try:
                user = User.objects.get(email=obj.email)
                url = reverse('admin:auth_user_change', args=[user.id])
                profile_info = f"{user.username} ({user.first_name} {user.last_name})"
                return format_html('<a href="{}">{}</a>', url, profile_info)
            except User.DoesNotExist:
                return 'Not a registered user'
            except User.MultipleObjectsReturned:
                users = User.objects.filter(email=obj.email)
                links = []
                for user in users:
                    url = reverse('admin:auth_user_change', args=[user.id])
                    links.append(format_html('<a href="{}">{}</a>', url, user.username))
                return format_html('Multiple users: {}', ', '.join(links))
        return 'No email provided'
    linked_user_detail.short_description = 'Registered User Account'


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


# Customize the User admin to show date_joined in list view
class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')
    list_filter = BaseUserAdmin.list_filter + ('date_joined',)
    ordering = ('-date_joined',)  # Default to newest first

# Unregister the default User admin and register our custom one
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass
admin.site.register(User, CustomUserAdmin)


@admin.register(SpamTrapEntry)
class SpamTrapEntryAdmin(admin.ModelAdmin):
    list_display = ('source', 'email_normalized', 'ip_address', 'reason', 'created_at')
    list_filter = ('source', 'reason', 'created_at')
    search_fields = ('email_normalized', 'email_raw', 'ip_address', 'user_agent', 'reason')
    readonly_fields = ('created_at',)
