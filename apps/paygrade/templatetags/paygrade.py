from django import template
from django.core.urlresolvers import reverse
from django.conf import settings
import json

register = template.Library()

@register.simple_tag
def min_pay_ajax_endpoint(service):
    """Includes the endpoint for getting the minimum pay by ajax.
    Usage:
        {% min_ajax_endpoint service %}
    """
    url_name = settings.PAY_GRADE_REVERSE_URL % {'service': service.key}
    return reverse(url_name)

@register.simple_tag
def paygrade_filter_fields(service):
    """
    Outputs a javascript array containing the filter fields
    for working out the paygrade for this service.
     
    Usage:
        var filter_fields= {% paygrade_filter_fields service %}; 
    """
    return json.dumps(service.pay_grade_model.filter_fields)
