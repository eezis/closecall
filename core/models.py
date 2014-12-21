from django.db import models


# Abstract Class for most common fields
class BaseFields(models.Model):
    tags = models.CharField(null=True, blank=True , max_length=120)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True



class UserInput(models.Model):
    subject = models.CharField(null=True, blank=True, max_length=150)
    first = models.CharField(null=True, blank=True, max_length=50, verbose_name="First Name")
    last = models.CharField(null=True, blank=True, max_length=50, verbose_name="Last Name")
    email = models.CharField(null=True, blank=True, max_length=150, verbose_name="Email Adress")
    message = models.TextField(null=True, verbose_name="Your comment, question, or feedback")
    created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        ordering = ['-created']


    def __unicode__(self):
        if self.subject is None:
            return 'No subject'
        else:
            return self.subject

