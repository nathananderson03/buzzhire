from rest_framework import mixins
from rest_framework import viewsets

class ViewAndDeleteViewset(mixins.DestroyModelMixin, viewsets.ReadOnlyModelViewSet):
  """A viewset to view & delete but not modify things"""
  pass

class RetrieveViewset(mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """A viewset for retrieving single objects.
    Use this viewset with apps.api.routers.SingleObjectFriendlyRouter
    for nicer routing.
    
    """
    detail_root = True


class RetrieveAndUpdateViewset(mixins.UpdateModelMixin,
                               RetrieveViewset):
    """A viewset for retrieving/updating single objects.
    Use this viewset with apps.api.routers.SingleObjectFriendlyRouter
    for nicer routing.
    
    """
    pass


class CreateUpdateNotDestroyViewset(mixins.CreateModelMixin,
                                    mixins.RetrieveModelMixin,
                                    mixins.UpdateModelMixin,
                                    mixins.ListModelMixin,
                                    viewsets.GenericViewSet):
    """Viewset which just leaves out the deletion capability from
    a standard ModelViewSet.
    """
    pass


class DateSliceMixin(object):
    """Mixin for Views/Viewsets wishing to implement a past/future 
    dateslice API.
    
    Requires that the queryset being used has the appropriate past()/future()
    methods on it.
    
    If the Viewset overrides get_queryset, be sure to called
    self.datesliced_queryset() before returning the queryset.
    
    """
    def get_queryset(self):
        queryset = super(DateSliceMixin, self).get_queryset()
        queryset = self.datesliced_queryset(queryset)
        return queryset

    def datesliced_queryset(self, queryset):
        """Filter the queryset by past/future, if the queryset arguments
        are supplied.
        """
        if self.request.GET.get('dateslice') == 'future':
            queryset = queryset.future()
        elif self.request.GET.get('dateslice') == 'past':
            queryset = queryset.past()
        return queryset
