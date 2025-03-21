"""Настройки для импорта данных из CSV-файлов."""

from reviews.models import Category, Comment, Genre, Review, Title
from users.models import User

from api_yamdb.settings import CSV_DATA_PATH

BULK_CREATE_BATCH_SIZE = 300


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
            'author': ('author', User),
            'title': ('title_id', Title),
            'text': 'text',
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
            'review': ('review_id', Review),
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
