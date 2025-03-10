from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (
    CreateModelMixin, ListModelMixin, DestroyModelMixin
)


class CreateListDestroyViewSet(
    CreateModelMixin, ListModelMixin,
    DestroyModelMixin, GenericViewSet
):
    """Класс для создания, просмотра и удаления объектов."""
