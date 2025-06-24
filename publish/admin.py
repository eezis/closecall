from django.contrib import admin

# Register your models here.
from .models import Announcement, BlogPost, InTheNews

# Register your models here.

class BlogPostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Announcement)
admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(InTheNews)