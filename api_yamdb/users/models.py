"""Модели приложения users."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.v1.validators import validator_forbidden_name

from .managers import CustomUserManager


class User(AbstractUser):
    """Расширенная модель пользователя."""

    username = models.CharField(
        max_length=settings.USERNAME_FIELD_LENGTH,
        unique=True,
        validators=[
            UnicodeUsernameValidator(),
            validator_forbidden_name
        ],
        verbose_name=_('Имя пользователя')
    )
    email = models.EmailField(
        unique=True,
        verbose_name=_('Адрес электронной почты')
    )

    bio = models.TextField(
        blank=True,
        verbose_name=_('Биография')
    )

    class RoleChoices(models.TextChoices):
        USER = settings.DEFAULT_USER_ROLE, _("Пользователь")
        MODERATOR = settings.MODERATOR_ROLE, _("Модератор")
        ADMIN = settings.ADMIN_ROLE, _("Администратор")

    role = models.CharField(
        max_length=settings.ROLE_FIELD_LENGTH,
        choices=RoleChoices.choices,
        blank=True,
        default=RoleChoices.USER,
        verbose_name=_('Роль пользователя')
    )

    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        """Meta."""
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ('username',)

    def __str__(self):
        return f'username пользователя: {self.username}'

    @property
    def is_admin(self):
        return self.role in (settings.ADMIN_ROLE,) or self.is_superuser

    @property
    def is_moderator(self):
        return self.role in (settings.MODERATOR_ROLE,)
