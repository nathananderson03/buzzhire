from rest_framework import permissions


class FreelancerOnlyPermission(permissions.BasePermission):
    """
    Permission check that the user is a freelancer.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and request.user.is_freelancer
