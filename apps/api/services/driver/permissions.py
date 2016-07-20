from rest_framework import permissions


class DriverOnlyPermission(permissions.BasePermission):
    """
    Permission check that the user is a driver.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.is_driver
