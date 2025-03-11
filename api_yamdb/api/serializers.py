from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title


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
        return obj.average_rating


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
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'text', 'author', 'pub_date',)
        read_only_fields = ('title', 'review', 'pub_date',)
        model = Comment


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username',
        default=serializers.CurrentUserDefault()
    )

    def validate(self, data):

        if self.context['request'].method != "PATCH" and (
            Review.objects.filter(
                author=self.context['request'].user,
                title=self.context['title_id']
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы можете написать только один отзыв к этому произведению.')
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date',)
        read_only_fields = ('title', 'pub_date',)
        model = Review
