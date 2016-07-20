from rest_framework import permissions


class ClientOnlyPermission(permissions.BasePermission):
    """
    Permission check that the user is a client.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.is_client

class ClientOrAdminOnlyPermission(permissions.BasePermission):
    """
    Permission check that the user is a client, or admin.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and (request.user.is_client or
                                                    request.user.is_admin)
