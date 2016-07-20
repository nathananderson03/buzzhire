from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import User
from .push import ParseConnection, CLIENT_APP, FREELANCER_APP

# class UserNotificationSettings(models.Model):
#     """Settings for each user related to notifications.
#     """
#     user = models.OneToOneField(User, related_name='notification_settings')


class NotificationQuerySet(models.QuerySet):
    "Custom queryset for Notifications."

    def for_user(self, user):
        "Filters by notifications for the current user."
        return self.filter(user=user).filter(datetime_deleted=None)


class Notification(models.Model):
    """A notification is a message sent by the system to a particular user.
    Optionally, it is linked by a generic relation.
    NB at present the notifications are always linked to job requests.  While
    the website doesn't mind what kind of object it's linked to, the mobile app
    may need to be adjusted if we link to other kinds of model instance.
    """
    message = models.TextField()
    category = models.CharField(max_length=30,
                    help_text='What kind of notification this is.')

    user = models.ForeignKey(User, related_name='notifications')

    datetime_created = models.DateTimeField(auto_now_add=True)
    datetime_deleted = models.DateTimeField(null=True, blank=True)

    # Optionally, relate the notification to another model
    content_type = models.ForeignKey(ContentType, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        created = not self.pk
        super(Notification, self).save(*args, **kwargs)
        # If the Notification is being created, send as a push notification too
        if created:
            self.send_as_push()

    def send_as_push(self):
        """Sends the notification as an push notification."""

        # Select the app to push to depending on the user
        app = FREELANCER_APP if self.user.is_freelancer else CLIENT_APP

        # TODO - this should be sent to the queue instead,
        # in case of network failure?
        connection = ParseConnection(app)
        connection.push_message(self.message,
                                self.user,
                                self.category,
                                self.content_type.model,
                                self.object_id)

    def __unicode__(self):
        return "%s..." % self.message[:15]

    objects = NotificationQuerySet.as_manager()

    class Meta:
        ordering = ('-datetime_created',)

# def dispatch_notifications(user, category, context={},
#                            related_object=None):
#     """Dispatches any notifications the user has opted in to, including
#     emails and push notifications.
#     """
#     # Create notification instance
#     notification = Notification(
#         user=user,
#         category=category,
#         message='',  # TODO
#         related_object=related_object,
#     )
#     notification.save()
#
#     # If the user has email notifications enabled
#     # Detect email callback for the supplied category
#     # Send email (via huey)
#     notification.send_as_email()
#
#     # If the user has push notifications enabled
#     # Detect push callback for the supplied category
#     # Send push notification via huey
#     notification.send_as_push()
