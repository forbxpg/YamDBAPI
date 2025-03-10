"""Настройки для импорта данных из CSV-файлов."""
from django.contrib.auth import get_user_model

from reviews.models import Review, Title, Category, Genre, Comment
from api_yamdb.settings import CSV_DATA_PATH


User = get_user_model()


BULK_CREATE_BATCH_SIZE = 150


CSV_MAPPING = {
    'users': {
        'model': User,
        'fields': {
            'id': 'id',
            'username': 'username',
            'email': 'email',
            'role': 'role',
            'bio': 'bio',
            'first_name': 'first_name',
            'last_name': 'last_name',
        },
        'path': str(CSV_DATA_PATH / 'users.csv'),
    },
    'category': {
        'model': Category,
        'fields': {
            'id': 'id',
            'name': 'name',
            'slug': 'slug'
        },
        'path': str(CSV_DATA_PATH / 'category.csv'),
    },
    'genre': {
        'model': Genre,
        'fields': {
            'id': 'id',
            'name': 'name',
            'slug': 'slug'
        },
        'path': str(CSV_DATA_PATH / 'genre.csv'),
    },
    'titles': {
        'model': Title,
        'fields': {
            'id': 'id',
            'name': 'name',
            'year': 'year',
            'category': ('category', Category),
        },
        'path': str(CSV_DATA_PATH / 'titles.csv'),
    },
    'review': {
        'model': Review,
        'fields': {
            'id': 'id',
            'title_id': ('title_id', Title),
            'text': 'text',
            'author': ('author', User),
            'score': 'score',
            'pub_date': 'pub_date',
        },
        'path': str(CSV_DATA_PATH / 'review.csv'),
    },
    'comments': {
        'model': Comment,
        'fields': {
            'id': 'id',
            'author': ('author', User),
            'review_id': ('review_id', Review),
            'pub_date': 'pub_date',
            'text': 'text',
        },
        'path': str(CSV_DATA_PATH / 'comments.csv'),
    },
}

M2M_MODELS_MAPPING = {
    'genre_title': {
        'model': (
            ('title_id', Title),
            ('genre_id', Genre),
        ),
        'fields': {
            'id': 'id',
            'title_id': 'title_id',
            'genre_id': 'genre_id',
        },
        'path': str(CSV_DATA_PATH / 'genre_title.csv'),
        'related_model_name': 'genre',
    },
}
