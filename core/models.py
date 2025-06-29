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
    email = models.CharField(null=True, blank=True, max_length=150, verbose_name="Email Address")
    message = models.TextField(null=True, verbose_name="Your comment, question, or proposal")
    created = models.DateTimeField(auto_now_add=True, null=True)


    class Meta:
        ordering = ['-created']


    def __unicode__(self):
        if self.subject is None:
            return 'No subject'
        else:
            return self.subject


class Product(BaseFields):
    name = models.CharField(max_length=200)
    description = models.TextField()
    amazon_asin = models.CharField(max_length=20, unique=True, help_text="Amazon Standard Identification Number")
    amazon_url = models.URLField(max_length=500, help_text="Full Amazon product URL")
    category = models.CharField(max_length=50, choices=[
        ('tires', 'Tires'),
        ('helmets', 'Helmets'),
        ('cameras', 'Cameras'),
        ('lights', 'Lights'),
        ('accessories', 'Accessories'),
        ('safety', 'Safety Equipment'),
    ])
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=500, null=True, blank=True)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    order = models.IntegerField(default=0, help_text="Display order (lower numbers appear first)")

    class Meta:
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def get_affiliate_url(self):
        """Generate Amazon affiliate URL with tracking ID"""
        # Extract ASIN from URL if needed
        if '/' in self.amazon_asin:
            asin = self.amazon_asin.split('/')[-2]
        else:
            asin = self.amazon_asin
        
        # Amazon affiliate tracking ID from the template
        tracking_id = "ccdb-16-20"
        return f"https://www.amazon.com/dp/{asin}/?tag={tracking_id}"

