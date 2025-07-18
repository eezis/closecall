from django.shortcuts import render
# from django.views.generic import TemplateView

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.views.generic.detail import DetailView

# RequestContext import removed - no longer needed in modern Django

from .models import InTheNews, Announcement, BlogPost

from core.views import ValidFormMixin, FilterToUserMixin, LoginRequiredMixin, admin_mailer
from django.urls import reverse, reverse_lazy
from django.core.mail import send_mail

from .forms import CreateBlogPostForm

from django.http import Http404

class NewsView(ListView):
    template_name = "publish/news.html"
    model = InTheNews
    context_object_name = "news_list"
    paginate_by = 5

    def get_queryset(self):
        return InTheNews.objects.filter(show_it=True)


def news_preview(request, news_id):
    # normally would be .get, but need to squeeze it into the for I n X iterable pattern
    # in the template.
    n = InTheNews.objects.filter(id=news_id)
    return render(request, 'publish/news.html', {'news_list': n})




"""
If there is an Announcement, I want it to show on every page I will try to make a
context processor to do that. It needs a RequestContext (generic views use those by default )
so I will use the list view and return a query. Then need to define the settings entry:
TEMPLATE_CONTEXT_PROCESSORS = ('publish.views.AnnouncementView',)

usage is in home but could be used to sitebase

"""

def AnnouncementView(request):
    # print('it ran')
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
    try:
        article = BlogPost.objects.get(slug=slug)
        return render(request, 'publish/article.html', {'article': article})
    except BlogPost.DoesNotExist:
        admin_mailer('Raising 404 for show_blog_post', 'Someone or something requested ' + unicode(request.get_full_path()) + ' add a redirect for that URL')
        raise Http404


def show_article(request, slug):
    # odd issue, with g+ getting appended, but can fix it here
    # /articles/cars-turning-left/https://plus.google.com/share/
    #  the trailing '/' gets lopped off before it gets here
    slug = slug.replace('/https://plus.google.com/share','')

    try:
        article = BlogPost.objects.get(slug=slug)

        if article.publish_it & article.post_is_public:
            return render(request, 'publish/show-article.html', {'article': article} )
        else:
            admin_mailer('Raising 404 for show_article', 'Some requested ' + unicode(slug) + ' and it is not publishable and public. Investigate.')
            raise Http404
    except BlogPost.DoesNotExist:
        # print(unicode(request.get_full_path()))
        admin_mailer('Raising 404 for show_article', 'Someone or something requested /articles/' + unicode(request.get_full_path()) + '/ add a redirect for that URL')
        raise Http404

def list_articles(request):
    articles = BlogPost.objects.filter(publish_it=True)
    return render(request, 'publish/articles.html', {'articles': articles} )



# class DetailBlogPostView(LoginRequiredMixin, DetailView):
#     model = BlogPost


# class DeleteBlogPostView(LoginRequiredMixin, DeleteView):
#     model = BlogPost
#     success_url = reverse_lazy('users-blogpost-list')



