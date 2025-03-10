"""Модели приложения users."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from api_yamdb.settings import ROLE_CHOICES, USERS_ROLE
from .manager import CustomUserManager
from .validators import CustomUsernameValidator


class User(AbstractUser):
    """Кастомный User."""
    username_validator = CustomUsernameValidator

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты'
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )

    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=USERS_ROLE['user'],
        verbose_name='Роль'
    )

    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        """Meta."""
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def superuser_is(self):
        return self.is_superuser

    @property
    def role_is(self):
        return self.role
