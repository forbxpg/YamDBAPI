"""Модели приложения reviews."""
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.text import Truncator, slugify
from django.utils.translation import gettext_lazy as _

# Пока на базовой
User = get_user_model()


class AbstractNameSlugBaseModel(models.Model):
    """
    Класс, определяющий абстрактную модель.

    Используется для создания моделей, имеющих name и slug.
    """

    name = models.CharField(
        max_length=settings.CHARFIELD_MAX_LENGTH,
        verbose_name=_('Название'),
    )
    slug = models.SlugField(
        max_length=settings.SLUG_FIELD_MAX_LENGTH,
        unique=True,
        editable=True,
        verbose_name=_('slug'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:settings.SLUG_FIELD_MAX_LENGTH]
        super().save(*args, **kwargs)


class Category(AbstractNameSlugBaseModel):
    """Модель категории."""

    class Meta(AbstractNameSlugBaseModel.Meta):
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')


class Genre(AbstractNameSlugBaseModel):
    """Модель жанра."""

    class Meta(AbstractNameSlugBaseModel.Meta):
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        _('Название'),
        max_length=settings.CHARFIELD_MAX_LENGTH,
    )
    year = models.IntegerField(
        _('Год выпуска'),
        validators=[
            MinValueValidator(settings.MIN_YEAR),
            MaxValueValidator(settings.MAX_YEAR),
        ]
    )
    description = models.TextField(
        _('Описание'),
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name=_('Жанр'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='titles',
        verbose_name=_('Категория'),
        db_index=True,
    )

    class Meta:
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')

    def __str__(self):
        return self.name


class Review(models.Model):
    """Модель отзыва."""

    class Meta(AbstractNameSlugBaseModel.Meta):
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')


class Comment(models.Model):
    """Модель комментария."""

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE
    )
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE
    )
    text = models.TextField(
        _('Текст комментария'),
        max_length=settings.CHARFIELD_MAX_LENGTH,
    )
    pub_date = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        default_related_name = 'comments'

    def __str__(self):
        desc = (
            f'Автор: {self.author}, произведение: {self.title}, ',
            f'Комментарий: {self.text}'
        )
        return Truncator(desc).words(settings.NAME_FIELD_TRUNCATOR)