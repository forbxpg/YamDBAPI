"""Модели приложения users."""
from time import timezone

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models
from django.utils import timezone

from .validators import CustomUsernameValidator


class UserManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')
        user = self.model(
            email=self.normalize_email(email).lower(),
            username=username,
            password=password
        )
        user.set_password(password)
        # if user.role == user.ROLE_CHOICES[2][0]:
        #   user.is_staff = True
        user.save(using=self._db)
        return user

    # def create_moderator(self, email, username, password=None):
    #     user = self.create_user(
    #         email=email,
    #         username=username,
    #         password=password
    #     )
    #     user.role = user.ROLE_CHOICES[1][0]
    #     user.save(using=self._db)
    #     return user

    # def create_admin(self, email, username, password=None):
    #     user = self.create_user(
    #         email=email,
    #         username=username,
    #         password=password
    #     )
    #     user.role = user.ROLE_CHOICES[2][0]
    #     user.is_staff = True
    #     user.save(using=self._db)
    #     return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email=email,
            username=username,
            password=password
        )
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username_validator = CustomUsernameValidator

    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name='username'
    )
    email = models.EmailField(
        max_length=254,
        unique=True,
        verbose_name='email'
    )
    first_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='first_name'
    )
    last_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        verbose_name='last_name'
    )
    bio = models.TextField(
        blank=True,
        null=True,
        verbose_name='Биография'
    )
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(default=timezone.now)

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
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
