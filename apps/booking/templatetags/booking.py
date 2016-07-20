from django import template
from ..models import Booking, Availability, Invitation
from ..forms import AvailabilityForm

register = template.Library()

@register.filter
def booking_exists_for_freelancer(job_request, freelancer):
    """Returns whether or not the freelancer is booked onto
    this job request.
    
    Usage:
        {% if job_request|booking_exists_for_freelancer:freelancer %}
            <p>Booking exists!</p>
        {% endif %}
    """
    return Booking.objects.filter(jobrequest=job_request,
                                  freelancer=freelancer).exists()

@register.filter
def invitation_exists_for_freelancer(job_request, freelancer):
    """Returns whether or not the freelancer has an invitation for
    this job request.
    
    Usage:
        {% if job_request|invitation_exists_for_freelancer:freelancer %}
            <p>Invitation exists!</p>
        {% endif %}
    """
    return Invitation.objects.filter(jobrequest=job_request,
                                  freelancer=freelancer).exists()

@register.filter
def invitation_for_freelancer(job_request, freelancer):
    """Returns the invitation the freelancer has received for
    this job request.
    
    If the invitation doesn't exist, returns None.
    
    Usage:
        {% with job_request|invitation_for_freelancer:freelancer as invitation %}
            <p>Invitation is {{ invitation }}!</p>
        {% endif %}
    """
    try:
        return Invitation.objects.get(jobrequest=job_request,
                                      freelancer=freelancer)
    except Invitation.DoesNotExist:
        return None


@register.filter
def availability_form_for_freelancer(freelancer):
    """Returns an availability form for the supplied freelancer,
    or False if it hasn't been filled out yet.
    """
    try:
        availability = freelancer.availability
    except Availability.DoesNotExist:
        return False
    return AvailabilityForm(instance=availability)


@register.assignment_tag(takes_context=True)
def freelancer_open_invitations_count(context):
    # TODO - this would be a good candidate for caching
    return Invitation.objects.can_be_applied_to_by_freelancer(
                                context['request'].user.freelancer).count()

