"""API Views."""
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import Category, Genre, Review, Title

from .mixins import CreateListDestroyViewSet
from .pagination import BaseLimitOffsetPagination
from .permissions import CommentReviewPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleReadSerializer, TitleWriteSerializer)


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Title.

    Предоставляет CRUD-операции для объектов модели.
    Права доступа на добавление/изменение только для админов.
    """

    queryset = Title.objects.prefetch_related(
        'genre').select_related('category').annotate(
            average_rating=Avg('reviews__score'))
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = (
        'name', 'genre__slug',
        'category__slug', 'year',
    )
    pagination_class = BaseLimitOffsetPagination

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleWriteSerializer
        return TitleReadSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """
    ViewSet для модели Category.

    Предоставляет операции создания, просмотра и удаления объектов.
    """

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = BaseLimitOffsetPagination


class GenreViewSet(CreateListDestroyViewSet):
    """
    ViewSet для модели Genre.

    Предоставляет операции создания, просмотра и удаления объектов.
    """

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = BaseLimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, CommentReviewPermission)
    pagination_class = BaseLimitOffsetPagination

    def review_obj(self):
        """Получает объект отзыва из url."""
        review = get_object_or_404(Review, pk=self.kwargs['review_id'])
        return review

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            review=self.review_obj(),
        )

    def get_queryset(self):
        return self.review_obj().comments.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""

    serializer_class = ReviewSerializer
    pagination_class = BaseLimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, CommentReviewPermission)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def title_obj(self):
        """Получает объект произведения из url."""
        return get_object_or_404(Title, pk=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(
            author=self.request.user,
            title=self.title_obj(),
        )

    def get_queryset(self):
        return self.title_obj().reviews.all()

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['title_id'] = self.kwargs['title_id']
        return context
