from django import template
from ..utils import PaymentAPI


register = template.Library()

@register.simple_tag
def payment_client_token(person):
    """Generates a client token based on the person provided.
    See utils.PaymentAPI.generate_client_token() for docs on the person.
    
    Usage:
    
        {% payment_client_token person %}
    """

    return PaymentAPI().generate_client_token(person)
