from django.db import models

# Create your models here.


class Announcement(models.Model):
    """
    This is for general news that can get loaded at the home page (for logged in and anonymous users)
    It's a short, quick hit kind of thing; the site will be down, we need to raise funds,
    we now have 100 users, etc.
    """
    the_announcement = models.TextField()
    start_on_date = models.DateField(null=True)
    end_on_date = models.DateField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Announcement"
        verbose_name_plural = "Announcements"

    def __unicode__(self):
        return self.the_announcement[:40]


class BlogPost(models.Model):
    """
    This is good old fashioned blog post, my thoughts or guest thoughts
    """
    title = models.CharField(max_length=150)
    the_post = models.TextField()
    tags = models.CharField(null=True, blank=True , max_length=50)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        verbose_name = "Blog Post"
        verbose_name_plural = "Blog Posts"

    def __unicode__(self):
        return self.title


class InTheNews(models.Model):
    """
    This is like the R-Bloggers thing. Write a summary, then
    paste a link to an article or post
    """
    title = models.CharField(max_length=150)
    summary = models.TextField()
    url = models.CharField(null=True, blank=True, max_length=250)
    tags = models.CharField(null=True, blank=True, max_length=50)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)


    class Meta:
        verbose_name = "In The News"
        verbose_name_plural = "In The News"
        ordering = ['-created']

    def __unicode__(self):
        return self.title
