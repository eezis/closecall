from django.conf.urls import patterns, url
from views import CreateBlogPostView, ListBlogPostView, UpdateBlogPostView #, DetailBlogPostView, DeleteBlogPostView

urlpatterns = patterns('',
    url(r'^list/$', ListBlogPostView.as_view(), name='users-blogpost-list'),
    url(r'^create/$', CreateBlogPostView.as_view(), name='create-blogpost'),
    # url(r'^detail/(?P<pk>\d+)/$', DetailBlogPostView.as_view(), name='blogpost-detail'),
    url(r'^update/(?P<pk>\d+)/$', UpdateBlogPostView.as_view(), name='update-blogpost'),
    url(r'^article/(?P<slug>.*)/$', 'publish.views.show_blog_post', name='show-blog-post'),
    # url(r'^delete/(?P<pk>\d+)/$', DeleteBlogPostView.as_view(), name='delete-blogpost'),
    # # this is for showing incidents that I wish to expose for a special reason (like link to it from a news story)
    # # the linking mecanims fake-2934 = incident.pk is mapped manually (for now) in a dictionary in the view
    # url(r'^show/([A-Z0-9-]{13})/$', 'incident.views.show_this_incident', name="show-specific-incident"),
    # # url(r'^show-detail/(?P<pk>\d+)/$', 'incident.views.show_this_incident_for_authed_users', name="show-specific-incident"),
    # url(r'^show-detail/(?P<incident_id>\d+)/$', 'incident.views.show_this_incident_for_authed_users', name="show-specific-incident"),

    )

