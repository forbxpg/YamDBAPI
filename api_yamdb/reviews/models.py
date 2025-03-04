"""Модели приложения reviews."""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        verbose_name=_('slug'),
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


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


class GenreTitle(models.Model):
    """Таблица связей Genre и Title."""

    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name=_('Жанр'),
    )
    title = models.ForeignKey(
        'Title',
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        verbose_name=_('Произведение')
    )


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
    rating = models.IntegerField(
        _('Рейтинг'),
        blank=True,
        null=True,
        validators=[
            MinValueValidator(settings.MIN_RATING),
            MaxValueValidator(settings.MAX_RATING),
        ]
    )
    genre = models.ManyToManyField(
        Genre,
        related_name='titles',
        verbose_name=_('Жанр'),
        through=GenreTitle
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
