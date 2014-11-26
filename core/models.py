from django.db import models


# Abstract Class for most common fields
class BaseFields(models.Model):
    tags = models.CharField(null=True, blank=True , max_length=120)
    created = models.DateTimeField(auto_now_add=True, null=True)
    updated = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True