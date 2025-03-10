"""Кастомный user менеджер."""
from django.contrib.auth.models import BaseUserManager
from api_yamdb.settings import USERS_ROLE


class CustomUserManager(BaseUserManager):
    """Кастомный менеджер для модели User."""

    def create_user(self, username, email, password=None, **extra_fields):
        """Созание пользователя."""
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
        if user.role == USERS_ROLE['admin']:
            user.is_staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email=None, password=None,
                         **extra_fields):
        """Созание суперпользователя."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', USERS_ROLE['admin'])

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)
