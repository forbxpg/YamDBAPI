
from django.contrib.auth import get_user_model

from api_yamdb.settings import CSV_DATA_PATH
from reviews.models import Review, Title, Category, Genre, Comment


User = get_user_model()


CSV_MAPPING = {
    'category': {
        'model': Category,
        'fields': {
            'id': 'id',
            'name': 'name',
            'slug': 'slug'
        },
        'path': CSV_DATA_PATH / 'category.csv'
    },
    'genre': {
        'model': Genre,
        'fields': {
            'id': 'id',
            'name': 'name',
            'slug': 'slug'
        },
        'path': CSV_DATA_PATH / 'genre.csv'
    },
    'titles': {
        'model': Title,
        'fields': {
            'id': 'id',
            'name': 'name',
            'year': 'year',
            'category': ('category', Category),
        },
        'path': CSV_DATA_PATH / 'titles.csv'
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
        'path': CSV_DATA_PATH / 'comments.csv'
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
        'path': CSV_DATA_PATH / 'review.csv'
    },
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
        'path': CSV_DATA_PATH / 'users.csv'
    },
    'genre_title': {
        'path': CSV_DATA_PATH / 'genre_title.csv'
    },
}
