from __future__ import absolute_import
from html2text import HTML2Text
from django import template


register = template.Library()


@register.filter
def html2text(value):
    """
    Converts html to human-readable plain text.
    
    Usage:
       
       {{ html|html2text }}
       
    """
    # This specific library converts it to Markdown
    handler = HTML2Text()
    return handler.handle(value)
