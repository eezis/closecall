from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify

# Create your models here.

# Abstract Class for most common fields
class PublishBase(models.Model):
    tldr = models.CharField(null=True, blank=True, max_length=250)
    tags = models.CharField(null=True, blank=True , max_length=120)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True


class PublishLocation(PublishBase):
    zipcode = models.CharField(null=True, blank=True, max_length=20)
    city = models.CharField(null=True, blank=True, max_length=80)
    state = models.CharField(null=True, blank=True, max_length=80)
    country = models.CharField(null=True, blank=True, max_length=80)

    class Meta:
        abstract = True


class Announcement(PublishBase):
    """
    This is for general news that can get loaded at the home page (for logged in and anonymous users)
    It's a short, quick hit kind of thing; the site will be down, we need to raise funds,
    we now have 100 users, etc.
    """
    the_announcement = models.TextField()
    show_it = models.BooleanField(default=False)
    start_on_date = models.DateField(null=True, blank=True)
    end_on_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"
        ordering = ['-start_on_date', '-created',]

    def __unicode__(self):
        return self.the_announcement[:80]


class BlogPost(PublishBase):
    """
    Good old fashioned blog post model, my thoughts or guest thoughts
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(null=True)
    the_post = models.TextField(null=True)
    publish_date = models.DateField(null=True, blank=True)
    reviewed = models.BooleanField(default=False)
    post_is_public = models.BooleanField(default=True)
    publish_it = models.BooleanField(default=False, verbose_name="Publish This Post")
    social_buttons = models.BooleanField(default=True, verbose_name="Show Social-Sharing Buttons")

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"
        # ordering = ['-publish_date', '-created',]
        ordering = ['-created',]

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(BlogPost, self).save(*args, **kwargs)


class InTheNews(PublishLocation):
    """
    This is like the R-Bloggers thing. Write a summary, then
    paste a link to an article or post
    """
    title = models.CharField(max_length=150)
    summary = models.TextField()
    url = models.CharField(null=True, blank=True, max_length=250)
    occurred_on = models.DateField(null=True, blank=True)
    report_on = models.DateField(null=True, blank=True)
    source = models.CharField(null=True, blank=True, max_length=120)
    show_it = models.BooleanField(default=False, verbose_name='Publish/Make Visible at site')

    class Meta:
        verbose_name = "In The News"
        verbose_name_plural = "In The News"
        # if there is no report_on date, than we fall back to the day it was entered
        ordering = ['-report_on', '-created',]

    def __unicode__(self):
        return self.title
