from django.shortcuts import render
# from django.views.generic import TemplateView
from django.views.generic import ListView

from django.template import RequestContext

from models import InTheNews, Announcement

class NewsView(ListView):
    template_name = "publish/news.html"
    model = InTheNews
    context_object_name = "news_list"
    paginate_by = 5




"""
If there is an Announcement, I want it to show on every page I will try to make a
context processor to do that. It needs a RequestContext (generic views use those by default )
so I will use the list view and return a query. Then need to define the settings entry:
TEMPLATE_CONTEXT_PROCESSORS = ('publish.views.AnnouncementView',)

usage is in home but could be used to sitebase

"""

def AnnouncementView(request):
    # print 'it ran'
    return {'announcement': Announcement.objects.filter(show_it=True) }
