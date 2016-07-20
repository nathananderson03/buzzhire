from django import template
from apps.job.models import JobRequest
from ..models import BookingFeedback, \
    get_bookings_awaiting_feedback_for_freelancer, \
    get_job_requests_awaiting_feedback_for_client
from django.conf import settings
from apps.main.templatetags.icons import icon
from django.contrib.admin.templatetags.admin_list import items_for_result
from apps.core.utils import template_names_from_polymorphic_model
from django.template.loader import render_to_string


register = template.Library()

@register.filter
def client_feedback_needed(job_request):
    """Returns whether or not the client can give feedback on the job request.
    Note this doesn't check whether the client owns the job request.
    Usage:
        {% if object|client_feedback_needed %}
            ...
        {% endif %}
    """
    # Allow feedback on complete job requests that haven't already had feedback
    # TODO - this template tag is probably redundant now,
    # can just call the method
    return job_request.needs_feedback_from_client()


@register.filter
def freelancer_feedback_needed(booking):
    """Returns whether or not the freelancer can give feedback on
    the supplied booking.
    Note this doesn't check whether the freelancer owns the job request.
    Usage:
        {% if object|freelancer_feedback_needed %}
            ...
        {% endif %}
    """
    # Allow feedback on complete job requests that haven't already had feedback
    return booking.jobrequest.status == JobRequest.STATUS_COMPLETE and not \
            BookingFeedback.objects.freelancer_feedback_exists(
                                    booking.jobrequest, booking.freelancer)
@register.filter
def freelancer_feedback_exists(booking):
    """Returns whether or not the freelancer gave feedback on
    the supplied booking.
    Usage:
        {% if object|freelancer_feedback_exists %}
            ...
        {% endif %}
    """

    return BookingFeedback.objects.freelancer_feedback_exists(
                                    booking.jobrequest, booking.freelancer)


@register.inclusion_tag('feedback/includes/feedback.html')
def feedback_for_freelancer_own(booking):
    """Outputs the client's own feedback for a freelancer, given the booking.
    
    Usage:
    
        {% feedback_for_freelancer_own booking %}
    """
    try:
        feedback = BookingFeedback.objects.client_feedback_from_booking(booking)
    except BookingFeedback.DoesNotExist:
        feedback = None
    return {
        'object': feedback,
        'heading': 'Your feedback',
    }

@register.inclusion_tag('feedback/includes/feedback.html')
def feedback_for_client(booking):
    """Outputs the freelancer's feedback for a client, given the booking.
    
    Usage:
    
        {% feedback_for_client booking %}
    """
    try:
        feedback = BookingFeedback.objects.freelancer_feedback_from_booking(
                                                    booking)
    except BookingFeedback.DoesNotExist:
        feedback = None
    return {
        'object': feedback
    }


@register.inclusion_tag('feedback/includes/feedback_for_freelancer_all.html')
def feedback_for_freelancer_all(freelancer):
    """Outputs the all the client feedback for a freelancer.
    
    Usage:
    
        {% feedback_for_freelancer_all freelancer %}
    """
    return {
        'object_list': BookingFeedback.objects.feedback_for_freelancer(
                                                                    freelancer)
    }


def split_score(score):
    """Splits a score (which can be a decimal or integer) into 
    a list of constituent units.
    
    E.g.:
        split_score(3.7) = [1, 1, 1, 0.7, 0]
    """
    items = []
    for i in range(BookingFeedback.MAX_SCORE):
        difference = score - i
        if difference > 0:
            if difference < 1:
                items.append(difference)
            else:
                items.append(1)
        else:
            items.append(0)
    return items


@register.inclusion_tag('feedback/includes/feedback_score.html')
def feedback_score(score, for_email=False):
    """Outputs the given score using icons.
    
    Can optionally specify whether it's for including in an email.  If it is,
    the icons will be shown as images instead.
    
    Usage:
    
        {% feedback_score feedback.score %}
    """
    context = {'score': score,
               'for_email': for_email}
    if score:
        context['split_score'] = split_score(score)
    return context


@register.inclusion_tag('feedback/includes/feedback_score.html')
def average_score(score, for_email=False):
    """Outputs the average score using icons.

    Can optionally specify whether it's for including in an email.  If it is,
    the icons will be shown as images instead.

    
    Usage:
    
        {% average_score feedback.average_score %}
    """
    context = {'score': score,
               'for_email': for_email,
               'include_value': True}
    if score:
        context['split_score'] = split_score(score)
    return context


@register.inclusion_tag('feedback/includes/feedback_icon.html')
def feedback_icon(unit, for_email=False):
    """Outputs an icon or image suitable for the unit supplied;
    Unit is 0, 1 or a fraction.
    If for_email is True, output as an image instead.
    """
    if unit == 1:
        name = 'score_full'
    elif unit == 0:
        name = 'score_empty'
    else:
        name = 'score_half'
    context = {'for_email': for_email}
    if for_email:
        context['image_path'] = 'img/email/feedback/%s.png' % name
        context['base_url'] = settings.BASE_URL
    else:
        context['icon_name'] = name

    return context


@register.assignment_tag(takes_context=True)
def freelancer_backlog_count(context):
    # TODO - this would be a good candidate for caching
    return get_bookings_awaiting_feedback_for_freelancer(
                                    context['request'].user.freelancer).count()


@register.assignment_tag(takes_context=True)
def client_backlog_count(context):
    # TODO - this would be a good candidate for caching
    return get_job_requests_awaiting_feedback_for_client(
                                    context['request'].user.client).count()

@register.simple_tag
def booking_feedback_summary(booking):
    """Outputs a summary of the feedback for a booking.
    Usage:
    
        {% booking_feedback_summary booking %}
    """

    template_names = template_names_from_polymorphic_model(
                    booking.freelancer.__class__, '_booking_feedback_summary',
                    'includes')
    return render_to_string(template_names, {'booking': booking,
                                             'freelancer': booking.freelancer})
