from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string, select_template
from .utils import template_names_from_polymorphic_model
from smtplib import SMTPRecipientsRefused
import logging

logger = logging.getLogger('project')


def send_mail(to, subject, template_name, context, from_email=None):
    """
    Sends an email to the supplied email address, using
    the template name and context.
    The template name should not include the file type; instead,
    it will search for .html and .txt versions of the template.
    NB both html and text versions are required.
    
    Can optionally specify a from_email, otherwise it will use
    CONTACT_EMAIL in the settings.
    """
    # Make to a list, if it isn't already
    if not isinstance(to, (list, tuple)):
        to = [to]

    if not from_email:
        from_email = settings.CONTACT_FROM_EMAIL

    context['domain'] = settings.DOMAIN
    context['contact_email'] = settings.CONTACT_EMAIL

    content = {}
    for content_format in ('txt', 'html'):
        content[content_format] = render_to_string('%s.%s' % (template_name,
                                                              content_format),
                                                   context)
    msg = EmailMultiAlternatives(subject,
                                 content['txt'],
                                 settings.DEFAULT_FROM_EMAIL,
                                 to)
    msg.attach_alternative(content['html'], "text/html")
    try:
        msg.send()
    except SMTPRecipientsRefused:
        # This happens if the domain isn't recognised - we don't
        # want an exception here
        logger.error('Failed to send email "%s" to %s.' % (subject, to[0]))


# def render_model_for_email(instance, suffix):
#     """Returns a rendered version of the supplied model instance,
#     for inclusion in an email.
#
#     Arguments:
#
#         - instance: the model instance
#         - suffix: the suffix to add to the template name.
#
#     Example:
#
#         render_model_for_email(driver_job_request, '_freelancer') will look for
#         the template 'driver/email/includes/driverjobrequest_freelancer.html',
#         falling back to 'job/email/includes/jobrequest_freelancer.html'.
#     """
#     template_names = template_names_from_polymorphic_model(instance.__class__,
#                                                 suffix=suffix,
#                                                 subdirectory='email/includes')
#     # Pass the available base template to the context.  This allows
#     # templates to extend the base template specific to the model type,
#     # without us needing to create specific templates for each suffix
#     # for that type.  For example, we can create a specific base template
#     # for DriverJobRequest without needing to have a specific DriverJobRequest
#     # client template to extend it.
#     BASE_SUFFIX = '_base'
#     if suffix is not BASE_SUFFIX:
#         base_template = select_template(template_names_from_polymorphic_model(
#                                         instance.__class__,
#                                         suffix=BASE_SUFFIX,
#                                         subdirectory='email/includes')).name
#     return render_to_string(template_names, {'object': instance,
#                                              'base_template': base_template})
