"""Сериализаторы API."""
from unicodedata import category

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.db import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from .email_service import send_code_to_email
from .validators import username_validator


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
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
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
        read_only_fields = ('title', 'review', 'pub_date')
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault(),
    )

    def validate(self, data):
        if self.context['request'].method != 'PATCH' and (
                Review.objects.filter(
                    author=self.context['request'].user,
                    title=self.context['title_id'],
                ).exists()
        ):
            raise serializers.ValidationError(
                'Вы можете написать только один отзыв к этому произведению.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title', 'pub_date')
        model = Review


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        validators=[username_validator],
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_FIELD_MAX_LENGTH,
    )

    def validate(self, data):
        try:
            User.objects.get_or_create(
                username=data['username'],
                email=data['email'],
            )
        except IntegrityError:
            raise serializers.ValidationError(
                'Пользователь с таким именем или почтой уже существует'
            )

        return data

    def create(self, validated_data):
        username = validated_data['username']
        email = validated_data['email']

        user, _ = User.objects.get_or_create(
            username=username,
            email=email,
        )
        user.save()
        send_code_to_email(user)
        return user


class ObtainTokenSerializer(serializers.Serializer):
    """Сериализатор для получения JWT-токена."""

    username = serializers.CharField(
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        required=True,
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
        data['user'] = user
        return data

    def create(self, validated_data):
        user = validated_data['user']
        refresh = RefreshToken.for_user(user)
        access_str = str(refresh.access_token)
        return access_str


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели User."""

    username = serializers.CharField(
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        validators=[
            username_validator, UniqueValidator(
                queryset=User.objects.all(),
            ),
        ],
    )
    email = serializers.EmailField(
        max_length=settings.EMAIL_FIELD_MAX_LENGTH,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
            )
        ],
    )

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
