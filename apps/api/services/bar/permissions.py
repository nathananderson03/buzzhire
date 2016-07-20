from rest_framework import permissions
from ..models import BarFreelancer

class BarFreelancerOnlyPermission(permissions.BasePermission):
    """
    Permission check that the user is a bar staff.
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated() and \
                BarFreelancer.objects.filter(user=self).exists()
