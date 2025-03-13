"""Модели приложения reviews."""
from django.conf import settings
from django.core.validators import (
    MaxValueValidator, MinValueValidator
)
from django.db import models
from django.utils.text import Truncator, slugify
from django.utils.translation import gettext_lazy as _
from users.models import User


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

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:settings.SLUG_FIELD_MAX_LENGTH]
        super().save(*args, **kwargs)


class Category(AbstractNameSlugBaseModel):
    """Модель категории."""

    class Meta(AbstractNameSlugBaseModel.Meta):
        verbose_name = _('Категория')
        verbose_name_plural = _('Категории')

    def __str__(self):
        return f'Название категории: {self.name}'


class Genre(AbstractNameSlugBaseModel):
    """Модель жанра."""

    class Meta(AbstractNameSlugBaseModel.Meta):
        verbose_name = _('Жанр')
        verbose_name_plural = _('Жанры')

    def __str__(self):
        return f'Название жанра: {self.name}'


class Title(models.Model):
    """Модель произведения."""

    name = models.CharField(
        _('Название'),
        max_length=settings.CHARFIELD_MAX_LENGTH,
    )
    year = models.SmallIntegerField(
        _('Год выпуска'),
        validators=[
            MaxValueValidator(
                settings.MAX_YEAR,
                message=_('Год не может быть больше текущего')
            ),
        ],
    )
    description = models.TextField(
        _('Описание'),
        blank=True,
    )
    genre = models.ManyToManyField(
        Genre,
        verbose_name=_('Жанр'),
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Категория'),
        db_index=True,
    )

    class Meta:
        default_related_name = 'titles'
        verbose_name = _('Произведение')
        verbose_name_plural = _('Произведения')

    def __str__(self):
        return f'Название произведения: {self.name}'


class AbstractTextAuthorPubdateModel(models.Model):
    """
    Класс, определяющий абстрактную модель.

    Используется для создания моделей,
    имеющих поля text, author и pub_date.
    """
    text = models.TextField(
        _('Текст'),
        max_length=settings.CHARFIELD_MAX_LENGTH,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name=_('Автор')
    )
    pub_date = models.DateTimeField(
        _('Дата добавления'),
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Review(AbstractTextAuthorPubdateModel):
    """Модель отзыва."""

    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        verbose_name=_('Произведение'),
    )
    score = models.SmallIntegerField(
        _('Оценка'),
        validators=[
            MinValueValidator(
                settings.MIN_RATING,
                message=_('Оценка должна быть от 1 до 10')
            ),
            MaxValueValidator(
                settings.MAX_RATING,
                message=_('Оценка должна быть от 1 до 10')
            ),
        ]
    )

    class Meta(AbstractTextAuthorPubdateModel.Meta):
        default_related_name = 'reviews'
        verbose_name = _('Отзыв')
        verbose_name_plural = _('Отзывы')
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique_author_title'
            )
        ]

    def __str__(self):
        desc = (
            f'Автор: {self.author}, произведение: {self.title}, ',
            f'оценка: {self.score}, отзыв: {self.text}'
        )
        return Truncator(desc).words(settings.NAME_FIELD_TRUNCATOR)


class Comment(AbstractTextAuthorPubdateModel):
    """Модель комментария."""

    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        verbose_name=_('Отзыв'),
    )

    class Meta(AbstractTextAuthorPubdateModel.Meta):
        default_related_name = 'comments'
        verbose_name = _('Комментарий')
        verbose_name_plural = _('Комментарии')

    def __str__(self):
        desc = (
            f'Автор: {self.author}, произведение: {self.title}, ',
            f'Комментарий: {self.text}'
        )
        return Truncator(desc).words(settings.NAME_FIELD_TRUNCATOR)
