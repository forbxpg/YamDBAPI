from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from reviews.models import (
    Comment, Title, Category, Genre
)


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

    rating = serializers.SerializerMethodField(read_only=True)
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

    def get_rating(self, obj):
        """Возвращает рейтинг произведения."""
        pass


class TitleWriteSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Title.

    Преобразует данные для создания или обновления объектов модели.
    """

    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.only('slug'),
        slug_field='slug',
        many=True
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.only('slug'),
        slug_field='slug'
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


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('title', 'review', 'pub_date',)
        model = Comment
