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

register = template.Library()

@register.filter
def markdownify(text):
    # safe_mode governs how the function handles raw HTML
    return markdown.markdown(text, safe_mode='escape')


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


"""
Note: For the security-minded, it's also possible to change the escape behaviour of the markdown function to disallow raw HTML
from being passed through. This way, we can expose a Markdown form to our users without worrying that they will inject malicious
code into our pages! In the example above, I've used safe_mode = 'escape' which automatically escapes raw HTML to a safe equivalent.
"""