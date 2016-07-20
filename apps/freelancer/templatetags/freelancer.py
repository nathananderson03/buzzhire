from django import template
from django.core.urlresolvers import reverse
from ..utils import service_for_freelancer


register = template.Library()

PHOTO_DIMENSIONS = {
    'tiny': '20x20',
    'small': '54x70',
    'medium': '75x97',
    'large': '233x300',
}

@register.inclusion_tag('freelancer/includes/profile_photo.html')
def profile_photo(freelancer, size='medium', for_email=False):
    """Renders the freelancer's profile photo, or a default image.
    
    For emails, optionally provide the base_url.
    
    Usage:
        {% profile_photo object 'large' %}
    
    Or for emails:
    
        {% profile_photo object for_email=True %}
    
    """

    return {
        'object': freelancer,
        'dimensions': PHOTO_DIMENSIONS[size],
        'for_email': for_email,
    }


@register.filter
def freelancer_profile_menu_items(freelancer):
    """Returns list of menu items for the freelancer's profile.
    
    Each menu item is in the form (link_url, title, icon_name).
    """
    menu_items = [
        (reverse('freelancer_change'), 'Edit profile',
            'icon-freelancer_profile_change'),
        (reverse('freelancer_photo'), 'Photo', 'icon-photo'),
    ]
    # Give service a change to add extra menu items
    service = service_for_freelancer(freelancer)
    menu_items.extend(service.freelancer_additional_menu_items)
    return menu_items


@register.filter
def freelancer_service(freelancer):
    """Outputs the service for the freelancer."""
    return service_for_freelancer(freelancer)


@register.filter
def freelancer_service_key(freelancer):
    """Outputs the service key for the freelancer."""
    return service_for_freelancer(freelancer).key

