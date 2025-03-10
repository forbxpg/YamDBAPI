from django.db.models import Q
from rest_framework.permissions import SAFE_METHODS, BasePermission


class CommentReviewPermission(BasePermission):
    """Ограничение для модели Comment.

    К запросам PUT, PATCH, DELETE допускается только автор, модератор и админ.
    К запросам POST допускаются авторизованные пользователи.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        return True

    def has_object_permission(self, request, view, obj):
        if request.method not in SAFE_METHODS:
            return bool(
                obj.author == request.user
                or request.user.is_staff
                or request.user.groups.filter(
                    Q(name='moderator') | Q(name='admin')
                ).exists()
            )
