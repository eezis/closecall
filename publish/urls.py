from django.urls import path, re_path
from .views import (
    CreateBlogPostView, ListBlogPostView, UpdateBlogPostView, show_blog_post
)

urlpatterns = [
    path('list/', ListBlogPostView.as_view(), name='users-blogpost-list'),
    path('create/', CreateBlogPostView.as_view(), name='create-blogpost'),
    re_path(r'^update/(?P<pk>\d+)/$', UpdateBlogPostView.as_view(), name='update-blogpost'),
    re_path(r'^article/(?P<slug>.*)/$', show_blog_post, name='show-blog-post'),
]