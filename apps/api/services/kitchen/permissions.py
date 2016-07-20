from rest_framework import permissions
from ..models import KitchenFreelancer


class KitchenFreelancerOnlyPermission(permissions.BasePermission):
    """
    Permission check that the user is a kitchen staff.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and \
                KitchenFreelancer.objects.filter(user=self).exists()
