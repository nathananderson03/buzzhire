from django import template
from ..models import Driver


register = template.Library()

@register.filter
def driver_from_freelancer(freelancer):
    """Returns the driver, given the freelancer.
    
    Usage:
        {{ freelancer|driver_from_freelancer }}
    """
    return Driver.driver_from_freelancer(freelancer)
