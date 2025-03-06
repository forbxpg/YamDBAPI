"""Пагинация API."""
from django.conf import settings
from rest_framework.pagination import LimitOffsetPagination


class BaseLimitOffsetPagination(LimitOffsetPagination):
    """Базовый класс пагинации."""

    default_limit = settings.DEFAULT_PAGE_SIZE
    max_limit = settings.MAX_PAGE_SIZE
