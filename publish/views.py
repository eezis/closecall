from django.shortcuts import render
# from django.views.generic import TemplateView
from django.views.generic import ListView

from models import InTheNews

class NewsView(ListView):
    template_name = "publish/news.html"
    model = InTheNews
    context_object_name = "news_list"