"""Сериализаторы API."""
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .validators import validator_forbidden_name


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Category."""

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Genre."""

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.

    Преобразует данные для чтения или удаления объектов модели.
    """

    rating = serializers.IntegerField(read_only=True, default=None)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',
        )
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.

    Преобразует данные для создания или обновления объектов модели.
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        allow_empty=False,
        allow_null=False,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        allow_empty=False,
    )

    class Meta:
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )
        model = Title

    def to_representation(self, instance):
        return TitleReadSerializer(instance).data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        request = self.context['request']
        if request.method != 'PATCH' and (
                Review.objects.filter(
                    author=request.user,
                    title=request.parser_context['kwargs']['title_id'],
                ).exists()
        ):
            raise serializers.ValidationError(
                'Вы можете написать только один отзыв к этому произведению.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title',)
        model = Review


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.USERNAME_FIELD_LENGTH,
        validators=[UnicodeUsernameValidator(), validator_forbidden_name]
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_FIELD_MAX_LENGTH,
    )

    def validate(self, data):
        user_by_name = User.objects.filter(username=data['username']).first()
        user_by_email = User.objects.filter(email=data['email']).first()
        if user_by_name != user_by_email:
            error_msg = {}
            if user_by_name is not None:
                error_msg['username'] = (
                    'Пользователь с таким именем уже существует'
                )
            if user_by_email is not None:
                error_msg['email'] = (
                    'Пользователь с такой почтой уже существует'
                )
            raise serializers.ValidationError(detail=error_msg)
        return data


class ObtainTokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(
        max_length=settings.USERNAME_FIELD_LENGTH,
        validators=[UnicodeUsernameValidator(), validator_forbidden_name]
    )
    confirmation_code = serializers.CharField(
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        required=True,
    )

    def validate(self, data):
        user = get_object_or_404(User, username=data['username'])
        if not default_token_generator.check_token(
                user,
                data['confirmation_code'],
        ):
            raise serializers.ValidationError(
                'Неверный код подтверждения или '
                'имя пользователя.'
            )
        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    def validate(self, data):
        example_value = {
            'field_name': [
                'Введите поле пользователя.'
            ]
        }
        if not data:
            raise serializers.ValidationError(example_value)
        return data

    class Meta:
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role',)
        model = User


class MeSerializer(UserSerializer):
    """Сериализатор текущего юзера."""

    role = serializers.CharField(
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        read_only=True,
    )
