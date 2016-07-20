from django import template
from sorl.thumbnail.templatetags.thumbnail import ThumbnailNode
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings


register = template.Library()


class StaticThumbnailNode(ThumbnailNode):
    """Works the same as the thumbnail tag, but for static files.

    Note the use of the 'endthumbnail' (not 'endstaticthumbnail') closing tag.

    Usage:

        {% staticthumbnail 'path/to/static.jpg' '300x500' as im %}
            <img src='{{ im.url }}' width='{{ im.width }}'
                 height='{{ im.height }}'/>
        {% endthumbnail %}
    """

    error_msg = ('Syntax error. Expected: ``staticthumbnail source geometry '
                 '[key1=val1 key2=val2...] as var``')

    def __init__(self, parser, token):
        super(StaticThumbnailNode, self).__init__(parser, token)
        # Prepend the static url to the file path
        bits = token.split_contents()
        absolute_url = staticfiles_storage.base_url
        if absolute_url[0] == '/':
            # We need to convert it to a url
            absolute_url = settings.BASE_URL + absolute_url

        self.file_ = parser.compile_filter("'%s'|add:%s" % \
                                (absolute_url, bits[1]))


@register.tag
def staticthumbnail(parser, token):
    return StaticThumbnailNode(parser, token)
