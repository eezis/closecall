from django.shortcuts import render
# from django.views.generic import TemplateView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

from django.template import RequestContext

from models import InTheNews, Announcement, BlogPost

from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin, admin_mailer
from django.core.urlresolvers import reverse, reverse_lazy
from django.core.mail import send_mail

from forms import CreateBlogPostForm


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


class CreateBlogPostView(LoginRequiredMixin, ValidFormMixin, CreateView):
    model = BlogPost
    form_class = CreateBlogPostForm
    success_url = reverse_lazy('users-blogpost-list')

    def form_valid(self, form):
        # set the user so that is saved when the form is committed
        form.instance.user = self.request.user
        BlogPost = form.save(commit=True)
        return super(CreateBlogPostView, self).form_valid(form)


class UpdateBlogPostView(LoginRequiredMixin, ValidFormMixin, UpdateView):
    model = BlogPost
    form_class = CreateBlogPostForm
    success_url = reverse_lazy('users-blogpost-list')


class ListBlogPostView(LoginRequiredMixin, ListView):
    model = BlogPost
    context_object_name = 'post_list'

def show_blog_post(request,slug):
    article = BlogPost.objects.get(slug=slug)
    return render(request, 'publish/article.html', {'article': article})


def show_article(request, slug):
    article = BlogPost.objects.get(slug=slug)
    if article.publish_it & article.post_is_public:
        return render(request, 'publish/show-article.html', {'article': article} )
    else:
        return




# class DetailBlogPostView(LoginRequiredMixin, DetailView):
#     model = BlogPost


# class DeleteBlogPostView(LoginRequiredMixin, DeleteView):
#     model = BlogPost
#     success_url = reverse_lazy('users-blogpost-list')



