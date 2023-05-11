from rest_framework import permissions
from rest_framework.permissions import BasePermission

from users.models import User


class IsReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or (request.user.is_authenticated
                and request.user.role == User.UserRoles.ADMIN)
        )


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or (request.user.is_authenticated
                and request.user.role == User.UserRoles.MODERATOR)
        )


class IsStaffOrAuthorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or request.user.role == User.UserRoles.ADMIN
            or request.user.role == User.UserRoles.MODERATOR
            or obj.author == request.user
        )
