from django import template
from django.conf import settings


register = template.Library()


@register.filter
def is_in_dashboard(path):
    """Returns whether or not the supplied path should be treated
    as within the dashboard.  Used to decide whether or not to 
    show links as active.
    
    Usage:
    
        <a{% if request.path|is_in_dashboard %} class='active'{% endif %}>
    """
    return True


@register.simple_tag
def contact_email():
    """Returns the contact email.
    
    Usage:
    
        {% contact_email %}
    """
    return settings.CONTACT_EMAIL

@register.simple_tag
def contact_phone():
    """Returns the contact phone number.
    
    Usage:
    
        {% contact_phone %}
    """
    return settings.CONTACT_PHONE

@register.inclusion_tag("main/customer_service_chat.html")
def customer_service_chat():
    """Renders the chat widget.

    Usage:

        {% customer_service_chat %}
    """

    return