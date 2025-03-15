"""API Views."""
from http import HTTPStatus

from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Genre, Review, Title

from .email_service import send_code_to_email
from .filters import TitleFilter
from .pagination import BaseLimitOffsetPagination
from .permissions import (IsAdminModerAuthorOrReadOnly, IsAdminOnly,
                          IsAdminOrReadOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, MeSerializer, ObtainTokenSerializer,
                          ReviewSerializer, SignUpSerializer,
                          TitleReadSerializer, TitleWriteSerializer,
                          UserSerializer)
from .viewsets import CreateListDestroyViewSet


User = get_user_model()


class TitleViewSet(viewsets.ModelViewSet):
    """
    ViewSet для модели Title.

    Предоставляет CRUD-операции для объектов модели.
    Права доступа на добавление/изменение только для админов.
    """

    queryset = Title.objects.prefetch_related(
        'genre').select_related('category').annotate(
        rating=Avg('reviews__score'))
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    pagination_class = BaseLimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

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
    permission_classes = (IsAdminOrReadOnly,)
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
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'slug'
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    pagination_class = BaseLimitOffsetPagination


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Comment."""

    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminModerAuthorOrReadOnly)
    pagination_class = BaseLimitOffsetPagination
    http_method_names = ('get', 'post', 'patch', 'delete')

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


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Review."""

    serializer_class = ReviewSerializer
    pagination_class = BaseLimitOffsetPagination
    permission_classes = (
        IsAuthenticatedOrReadOnly, IsAdminModerAuthorOrReadOnly)
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


class APISignUpView(APIView):
    """Передать email и username, отправить код подтверждения."""

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        send_code_to_email(user)
        return Response(serializer.data, status=HTTPStatus.OK)


class TokenObtainView(APIView):
    """
    Получение JWT-токена в обмен на username и confirmation code.
    Права доступа: Доступно без токена.
    """

    def post(self, request):
        serializer = ObtainTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            User, username=serializer.validated_data['username'])
        refresh = RefreshToken.for_user(user)
        access_str = str(refresh.access_token)
        return Response({'token': access_str}, status=HTTPStatus.OK)


class UsersViewSet(viewsets.ModelViewSet):
    """ViewSet для модели Users."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = BaseLimitOffsetPagination
    permission_classes = (IsAdminOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    http_method_names = ('get', 'post', 'patch', 'delete')

    def perform_create(self, serializer):
        role = serializer.validated_data.get('role', 'user')
        if role in (settings.ADMIN_ROLE,):
            return serializer.save(is_staff=True, role=role)
        return serializer.save(is_staff=False, role=role)

    perform_update = perform_create

    @action(detail=False, methods=['get', 'patch'],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        example_value = {
            "field_name": [
                "string"
            ]
        }
        user = get_object_or_404(User, username=request.user.username)
        if request.method == 'PATCH':
            serializer = MeSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if not request.data:
                return Response(example_value,
                                status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
        else:
            serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
