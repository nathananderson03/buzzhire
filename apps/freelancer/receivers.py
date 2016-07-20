from django.dispatch import receiver
from django.db.models.signals import post_save
from apps.core.email import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Freelancer


@receiver(post_save)
def notify_personnel_on_freelancer_created(sender, instance, created, **kwargs):
    """Notifies the staff responsible for personnel (i.e. the jobs email)
    when a freelancer is created.
    """
    if created and isinstance(instance, Freelancer):
        subject = 'New freelancer sign up: %s' % instance.get_full_name()
        content = render_to_string(
            'freelancer/email/includes/freelancer_created.html',
            {'object': instance}
        )
        send_mail(settings.JOBS_EMAIL,
                  subject,
                  'email/base',
                  {'title': subject,
                   'content': content})


@receiver(post_save)
def welcome_freelancer_on_sign_up(sender, instance, created, **kwargs):
    "Sends a welcome email when a freelancer signs up."
    if created and isinstance(instance, Freelancer):
        subject = 'Welcome to BuzzHire!'
        content = render_to_string(
            'freelancer/email/includes/freelancer_welcome.html',
            {'object': instance}
        )
        send_mail(instance.user.email,
                  subject,
                  'email/base',
                  {'title': subject,
                   'content': content})
