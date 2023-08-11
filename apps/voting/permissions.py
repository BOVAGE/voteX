from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Voter


class IsVoter(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, Voter)
