"""API Views."""
from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from reviews.models import Category, Genre, Review, Title

from .mixins import CreateListDestroyViewSet
from .pagination import BaseLimitOffsetPagination
from .permissions import CommentReviewPermission, UserPermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ObtainTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)

User = get_user_model()


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
    http_method_names = ('get', 'post', 'patch', 'delete')

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


class APISignUpView(APIView):
    """Передать email и username, отправить код подтверждения."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=HTTPStatus.OK)


class TokenObtainView(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена.
    """

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            token = serializer.save()
        return Response({'Your token': token}, status=HTTPStatus.OK)


class UsersViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = BaseLimitOffsetPagination
    permission_classes = (UserPermission,)
    search_fields = ('username',)


class APIMeView(APIView):
    """APIMeView."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=HTTPStatus.OK)

    def patch(self, request):
        example_value = {
            "field_name": [
                "string"
            ]
        }
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True) and request.data:
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(example_value, status=status.HTTP_400_BAD_REQUEST)
