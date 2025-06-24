# http://www.jw.pe/blog/post/using-markdown-django-17/
"""
see comments at the link above, see this response
http://www.jw.pe/blog/post/markdown-speed-and-denormalisation/
"""
# https://docs.djangoproject.com/en/1.7/howto/custom-template-tags/

# The app that contains the custom tags must be in INSTALLED_APPS in order for the {% load %} tag to work.

# http://pythonhosted.org/Markdown/
# MARKDOWN SYNTAX http://daringfireball.net/projects/markdown/syntax

""" **** SECURITY ISSUE **** only use safe with internally controlled content ****  see note below"""


from django import template
import markdown
# from django.utils.safestring import SafeString

register = template.Library()

@register.filter
def markdownify(text):
    # return SafeString(markdown.markdown(text, safe_mode='escape'))
    # safe_mode governs how the function handles raw HTML
    # return markdown.markdown(text, safe_mode='escape')
    return markdown.markdown(text)


"""
Template Usage

{% load markdown_filter %}
<html>
...
  <div class="md-content">
    {{ my_markdown_content|markdownify|safe }}
  </div>
</html>
"""

# from users.models import UserProfile

# @register.filter
# def grabprofileid(req_user):
#     try:
#         print("grabprofileid has been called")
#         # return the userprofile of the requesting user
#         up = UserProfile.objects.get(user=req_user.id)
#         return up.id
#     except:
#         return None

"""

This was unnecessary: https://docs.djangoproject.com/en/1.7/topics/auth/customizing/#extending-the-existing-user-model

I used this instead: <li><a href="/user-profile-detail/{{user.profile.id}}" >Your Profile</a></li>

grabprofileid is used in _nav-right.html in order to get the user's UserProfile, it's criticl to load this file in the template!

{% load markdown_filter %}

        {% if user.is_authenticated %}

         <li class="dropdown">
            <a href="#" class="dropdown-toggle" data-toggle="dropdown"><span class="glyphicon glyphicon-cog white" style="padding: 2px 0 2px 0;"></span> <span class="caret"></span></a>
              <ul class="dropdown-menu" role="menu">
                <li><a href="/user-profile-detail/{{user|grabprofileid}}" >Your Profile</a></li>
                <li><a href="/accounts/logout/" >Logout</a></li>
              </ul>
          </li>

"""


"""
Note: For the security-minded, it's also possible to change the escape behaviour of the markdown function to disallow raw HTML
from being passed through. This way, we can expose a Markdown form to our users without worrying that they will inject malicious
code into our pages! In the example above, I've used safe_mode = 'escape' which automatically escapes raw HTML to a safe equivalent.
"""