"""Модели приложения users."""
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

from .validators import CustomUsernameValidator


class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username=username,
            email=self.normalize_email(email).lower(),
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    username_validator = CustomUsernameValidator

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='Адрес электронной почты:'
    )

    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )

    ROLE_CHOICES = (
        ('user', 'user'),
        ('moderator', 'moderator'),
        ('admin', 'admin'),
    )

    role = models.CharField(
        max_length=9,
        choices=ROLE_CHOICES,
        default=ROLE_CHOICES[0][0],
        verbose_name='роль'
    )

    REQUIRED_FIELDS = ['email']
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
