"""Модели приложения users."""
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager
from .validators import CustomUsernameValidator


class User(AbstractUser):
    """Расширенная модель пользователя."""
    username_validator = CustomUsernameValidator

    username = models.CharField(
        max_length=settings.USERNAME_FIELD_LENGTH,
        unique=True,
        verbose_name=_('Имя пользователя')
    )
    email = models.EmailField(
        max_length=settings.EMAIL_FIELD_MAX_LENGTH,
        unique=True,
        verbose_name=_('Адрес электронной почты')
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name=_('Биография')
    )

    role = models.CharField(
        max_length=settings.ROLE_FIELD_LENGTH,
        choices=settings.ROLE_CHOICES,
        blank=True,
        default=settings.USERS_ROLE['user'],
        verbose_name=_('Роль пользователя')
    )

    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        """Meta."""
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    @property
    def superuser_is(self):
        return self.is_superuser

    @property
    def role_is(self):
        return self.role
