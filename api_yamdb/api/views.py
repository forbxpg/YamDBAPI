from django.shortcuts import get_object_or_404
from rest_framework import viewsets

from api.permissions import CommentPermission
from api.serializers import CommentSerializer
from reviews.models import Review


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (CommentPermission,)

    def review_obj(self):
        """Получает объект отзыва из url."""
        return get_object_or_404(Review, pk=self.kwargs['review_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_obj(),
        )

    def get_queryset(self):
        return self.review_obj().comments.all()
