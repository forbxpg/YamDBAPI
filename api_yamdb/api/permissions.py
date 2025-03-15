"""Модуль для классов разрешений API."""
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminModerAuthorOrReadOnly(BasePermission):
    """Ограничение доступа для определенных ролей пользователей.

    К запросам PUT, PATCH, DELETE допускается только автор, модератор и админ.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated
                and (request.user.is_moderator or request.user.is_admin))
        )


class IsAdminOrReadOnly(BasePermission):
    """Ограничение доступа. Для всех только SAFE_METHODS, кроме админа."""

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (request.user.is_authenticated
                                                  and request.user.is_admin)


class IsAdminOnly(BasePermission):
    """Ограничение доступа. К запросам допускается только админ."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin
