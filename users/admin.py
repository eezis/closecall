from django.contrib import admin

# Register your models here.
from models import UserProfile, UserBlogProfile

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(UserBlogProfile)