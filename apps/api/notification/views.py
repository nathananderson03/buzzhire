from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import detail_route
from rest_framework.response import Response
from apps.notification.models import Notification
from apps.api.views import ViewAndDeleteViewset
from .serializers import NotificationSerializer
import datetime


class NotificationsForUserViewSet(ViewAndDeleteViewset):
    """All notifications for the currently logged in user.  Read only.
    
    ## Fields
    
    - `id` Unique id for the notification. Integer.
    - `category` A machine-readable name to identify what
       kind of notification this is.
    - `message` The text of the message.  
    - `datetime_created` Date and time of the notification, in UTC.
    - `datetime_created_localtime` Date and time of the notification in the
       site's local time.
    - `object_id` Notifications can optionally be
       associated with a model in the system, known as the 'related object'.
       Together, the object id and content type form a unique reference to
       the related object. Integer.
    - `content_type` The type of the related object.  String.  
    
    """
    serializer_class = NotificationSerializer

    permission_classes = (permissions.IsAuthenticated,)

    lookup_field = 'pk'

    def get_queryset(self):
        return Notification.objects.for_user(self.request.user)

    def destroy(self, request, pk=None):
        notification = self.get_object()
        assert(self.request.user == notification.user)
        # Not a real delete, but instead setting the 'read' flag
        # nothing should be deleted ever, to have a record of all
        # notifications sent out to freelancers so they can't claim
        # that they didn't get something later on
        notification.datetime_deleted = datetime.datetime.now()
        notification.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
