from django import template
from .. import services


register = template.Library()


@register.assignment_tag
def get_services():
    """Assignment tag for getting the registered services.
    
    Usage:
    
        {% get_services as services %}
        {% for service in services %}
            {# Do something #}
        {% endfor %} 
    """
    return services.values()
