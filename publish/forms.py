from django import forms
from django.forms import ModelForm

# from tinymce.widgets import TinyMCE
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget

from .models import BlogPost

class CreateBlogPostForm(ModelForm):
    publish_date = forms.DateField(input_formats=["%m/%d/%Y"], widget=forms.DateInput(format="%m/%d/%Y", attrs={'class': 'datePicker',}), label='Publication Date:')

    class Meta:
        model = BlogPost
        fields = ['title', 'the_post', 'tags', 'publish_date', 'publish_it', 'social_buttons', ]

        widgets={
            "the_post": SummernoteInplaceWidget(),
            "about_the_author": SummernoteInplaceWidget(),

            # doesn't seem to have support for placeholder text?
            # "what": SummernoteInplaceWidget(attrs={
            #     'placeholder': 'test',
            #     }),

        }
