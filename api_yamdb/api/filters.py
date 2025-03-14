"""Фильтры."""
from django_filters import rest_framework as api_filter
from reviews.models import Title


class TitleFilter(api_filter.FilterSet):
    """Фильтр для поиска для модели Title."""

    name = api_filter.CharFilter(field_name='name', lookup_expr='icontains')
    genre = api_filter.CharFilter(field_name='genre__slug')
    category = api_filter.CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
