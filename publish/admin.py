from django.contrib import admin

# Register your models here.
from models import Announcement, BlogPost, InTheNews

# Register your models here.

admin.site.register(Announcement)
admin.site.register(BlogPost)
admin.site.register(InTheNews)