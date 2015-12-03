from django.contrib import admin

# Register your models here.
from models import UserProfile, UserBlogProfile

# Register your models here.

class UserProfileAdmin(admin.ModelAdmin):
    search_fields = ['first', 'last', 'country', 'city', 'user__email' ]
    list_filter = ('country', 'state',)

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(UserBlogProfile)