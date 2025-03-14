"""Модуль для классов разрешений API."""
from django.conf import settings
from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminModerAuthorOrReadOnly(BasePermission):
    """Ограничение доступа для определенных ролей пользователей.

    К запросам PUT, PATCH, DELETE допускается только автор, модератор и админ.
    """

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (
                request.user.is_authenticated
                and (request.user.role_is == settings.MODERATOR_ROLE
                     or request.user.role_is == settings.ADMIN_ROLE)
            )
        )


class TitlePermission(BasePermission):
    """Ограничение для модели Title."""

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return (
                request.user.is_authenticated
                and request.user.role_is == 'admin'
                or request.user.is_superuser
            )
        return True

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return (
                request.user.is_authenticated
                and request.user.role_is == 'admin'
                or request.user.is_superuser
            )
        return True


class CategoryAndGenrePermission(BasePermission):
    """Ограничение для моделей Category и Genre."""

    def has_permission(self, request, view):
        if request.method not in SAFE_METHODS:
            return (
                request.user.is_authenticated
                and request.user.role_is == 'admin'
                or request.user.is_superuser
            )
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_authenticated
            and request.user.role_is == 'admin'
            or request.user.is_superuser
        )


class UserPermission(BasePermission):
    """Ограничение для модели User. К запросам допускается только админ."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role_is == 'admin'
            or request.user.is_superuser
        )
