"""Дополнительные команды для заполнения БД данными из csv."""
import csv

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from reviews.models import (
    Category, Genre, Title, Review, Comment
)
from api_yamdb.settings import CSV_DATA_PATH
from .csv_config import CSV_MAPPING
from .exceptions import CommandException


User = get_user_model()


MODEL_CONFIG = {
    'category': (Category, CSV_DATA_PATH / 'category.csv'),
    'genre': (Genre, CSV_DATA_PATH / 'genre.csv'),
    'titles': (Title, CSV_DATA_PATH / 'titles.csv'),
    'review': (Review, CSV_DATA_PATH / 'review.csv'),
    'comments': (Comment, CSV_DATA_PATH / 'comments.csv'),
    'genre_title': (None, CSV_DATA_PATH / 'genre_title.csv'),
    'users': (User, CSV_DATA_PATH / 'users.csv'),
}


class Command(BaseCommand):
    """
    Кастомная команда для заполнения БД данными из csv.

    Пример использования:
        python(3) manage.py db_fill --category - заполнение Category.
        python(3) manage.py db_fill --all - заполнение всех таблиц.
    """

    help = 'Команда, заполняющая БД данными из csv.'

    def add_arguments(self, parser):
        """Добавление аргументов для ввода в командной строке."""

        for db_table in CSV_MAPPING:
            if db_table != 'genre_title':
                parser.add_argument(
                    f'--{db_table}',
                    action='store_true',
                    help=f'Заполнение таблицы {db_table}',
                )
        parser.add_argument(
            '--genre_title',
            action='store_true',
            help='Заполнение ManyToMany связанных таблиц Genre, Title',
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Заполнение всех таблиц',
        )

    def handle(self, *args, **options):
        """
        Вся логика реализации заполнения.

        Работа по принципу ACID.
        Данные либо все заполнятся, либо нет.
        """
        try:
            with transaction.atomic():
                if options.get('all', False):
                    self.fill_all_tables()
                else:
                    self.fill_selected_tables(options)
            self.stdout.write(self.style.SUCCESS('Данные успешно заполнены!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка {e}'))

    def fill_all_tables(self):
        for db_table in CSV_MAPPING:
            if db_table != 'genre_title':
                self.fill_tables(db_table)
            else:
                self.fill_genre_title()

    def fill_selected_tables(self, options):
        fill_order = [
            'users',
            'category',
            'genre',
            'titles',
            'review',
            'comments',
            'genre_title',
        ]
        for db_table in fill_order:
            if options.get(db_table, False):
                if db_table != 'genre_title':
                    self.fill_tables(db_table)
                else:
                    self.fill_genre_title()

    def fill_tables(self, table_name):
        table = CSV_MAPPING.get(table_name)
        if not table:
            raise CommandException(f'Конфигурация для {table} не найдена')
        model = table.get('model')
        fields_map = table.get('fields')

        with open(table.get('path'), 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for line in reader:
                self.process_lines(model, fields_map, line)
            self.stdout.write('Таблицы заполнены!')

    def process_lines(self, model, fields_dict, line):

        model_fields = {}

        for field_key, field_value in fields_dict.items():
            if isinstance(field_value, tuple):
                relation_id, related_model_name = field_value
                model_fields[field_key] = related_model_name.objects.get(
                    id=line.get(relation_id)
                )
            else:
                model_fields[field_key] = line[field_value]

        try:
            model.objects.get_or_create(**model_fields)
        except Exception as e:
            self.stdout.write(
                self.style.WARNING(
                    f'Пропущена запись {model_fields}, ошибка {e}'
                )
            )

    def fill_genre_title(self):
        path = CSV_MAPPING['genre_title']['path']
        with open(path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for line in reader:
                title = Title.objects.get(id=line['title_id'])
                genre = Genre.objects.get(id=line['genre_id'])
                title.genre.add(genre)
        self.stdout.write('Таблица ManyToMany заполнена')
