from rest_framework.permissions import SAFE_METHODS, BasePermission


class CommentReviewPermission(BasePermission):
    """Ограничение для модели Comment.

    К запросам POST допускаются авторизованные пользователи.
    К запросам PUT, PATCH, DELETE допускается только автор, модератор и админ.
    """
    def has_permission(self, request, view):
        if request.method == 'POST':
            return bool(request.user and request.user.is_authenticated)
        return True

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or obj.author == request.user
            or (request.user.is_authenticated
                and request.user.role_is != 'user')
        )
