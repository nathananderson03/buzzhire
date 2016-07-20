from django.core.urlresolvers import NoReverseMatch
from rest_framework.routers import Route, DynamicDetailRoute
from rest_framework.compat import get_resolver_match, OrderedDict
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import routers
from rest_framework import views


class SingleObjectFriendlyRouter(routers.DefaultRouter):
    """A router that plays nicely with viewsets designed to
    interact with a single object, such as
    apps.api.views.RetrieveAndUpdateViewset.
    
    It will assign the detail view as the root url, so that the object can be
    accessed without passing a pk.
    
    The Viewset classes should define a get_object() method, and have
    a detail_root attribute that equals True.  
    """
    _detail_routes = [
        # Detail route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

    def __init__(self, *args, **kwargs):
        super(SingleObjectFriendlyRouter, self).__init__(*args, **kwargs)
        # Copy the default routes to a private attribute,
        # as we change the value of self.routes in get_routes
        self._routes = self.routes

    def get_routes(self, viewset):
        # Set self.routes to the default, or detail, depending
        # on whether the viewset declares that it should have a detail root.
        if getattr(viewset, 'detail_root', False):
            self.routes = self._detail_routes
        else:
            self.routes = self._routes
        return super(SingleObjectFriendlyRouter, self).get_routes(viewset)

    def get_api_root_view(self):
        # Most of this is copied from DefaultRouter.get_api_root_view(),
        # but it uses the detail urls for the relevant viewsets.
        api_root_dict = OrderedDict()
        for prefix, viewset, basename in self.registry:
            # Choose a root name depending on whether the viewset
            # declares that it should have a detail root.
            if getattr(viewset, 'detail_root', False):
                root_name = self._detail_routes[0].name
            else:
                root_name = self._routes[0].name

            api_root_dict[prefix] = root_name.format(basename=basename)

        class APIRoot(views.APIView):
            _ignore_model_permissions = True

            @classmethod
            def as_view(cls, **initkwargs):
                cls.extra_endpoints = initkwargs.pop('extra_endpoints')
                return super(APIRoot, cls).as_view(**initkwargs)

            def get(self, request, *args, **kwargs):
                ret = OrderedDict()
                namespace = get_resolver_match(request).namespace
                for key, url_name in api_root_dict.items():
                    if namespace:
                        url_name = namespace + ':' + url_name
                    try:
                        ret[key] = reverse(
                            url_name,
                            request=request,
                            format=kwargs.get('format', None)
                        )
                    except NoReverseMatch:
                        # Don't bail out if eg. no list routes exist, only detail routes.
                        continue

                # Add extra endpoints
                for local_path, url_name in self.extra_endpoints:
                    ret[local_path] = reverse(url_name,
                                              request=request)

                return Response(ret)

        return APIRoot.as_view(extra_endpoints=self.extra_endpoints)

    """extra_endpoints is a list of extra endpoints to be added to the
    self documenting API.
        
    Usage:
    
        class MyRouter(SingleObjectFriendlyRouter):
            extra_endpoints = [
                
            ] 
    """
    extra_endpoints = []
