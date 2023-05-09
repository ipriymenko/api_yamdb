from rest_framework import permissions
from rest_framework.permissions import BasePermission

from users.models import User


class IsOwnerOrHasAdminRole(BasePermission):

    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated
            and (
                request.user.is_superuser
                or request.user.role == User.UserRoles.ADMIN
            )
        )

