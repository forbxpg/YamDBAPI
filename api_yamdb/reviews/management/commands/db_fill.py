"""Дополнительные команды для заполнения БД данными из csv."""
import logging
from typing import Dict

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction

from ..services import (
    fill_many_to_many_tables,
    fill_simple_and_foreign_key_tables,
)
from ..csv_config import CSV_MAPPING, M2M_MODELS_MAPPING


logger = logging.getLogger('import')


User = get_user_model()


class Command(BaseCommand):
    """
    **Кастомная команда для заполнения БД данными из csv-файлов.**

    **Пример использования**:
    - `python(3) manage.py db_fill --category` - заполнение таблицы category.
    - `python(3) manage.py db_fill --all` - заполнение всех таблиц.

    **Ограничения**:
        **Заполнение должно происходить в строго-определенном порядке:**
        1) ***Если понадобится заполнить таблицу, в которой FK поле,
        то необходимо сначала заполнить таблицу, на которую ссылается поле.***
        **e.g**:
            - `python(3) manage.py db_fill --category`
            - `python(3) manage.py db_fill --title`
        2) ***Если понадобится заполнить таблицу, где поле имеет связь M2M,
        то необходимо сначала заполнить таблицу, которая имеет M2M поле,
        затем связанную.***
        **e.g**: (предполагается, что таблица category заполнена)
            - `python(3) manage.py db_fill --title`
            - `python(3) manage.py db_fill --genre_title`
    """

    help = 'Команда для заполнения таблиц в базе данных.'

    def add_arguments(self, parser):
        """Добавляет аргументы, используемые в команде."""

        for table in CSV_MAPPING:
            parser.add_argument(
                f'--{table}',
                action='store_true',
                help=f'Заполнение таблицы {table}',
            )
        for m2m_table in M2M_MODELS_MAPPING:
            parser.add_argument(
                f'--{m2m_table}',
                action='store_true',
                help=f'Заполнение таблицы {m2m_table}',
            )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Заполнение всех таблиц',
        )

    def handle(self, *args, **options):
        """
        Реализует заполнение базы данных.

        Реализует принцип атомарности транзакций.
        База данных не будет заполнена, если в csv имеются ошибки.
        """
        logger.info('Заполнение базы данных...')
        try:
            with transaction.atomic():
                if options.get('all', False):
                    self.fill_all_tables(
                        CSV_MAPPING, M2M_MODELS_MAPPING,
                    )
                else:
                    self.fill_selected_tables(
                        options, CSV_MAPPING, M2M_MODELS_MAPPING,
                    )
            self.stdout.write(self.style.SUCCESS('Данные успешно заполнены!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ошибка при заполнении: {e}'))

    def fill_all_tables(
        self,
        simple_model_mapping: Dict,
        m2m_model_mapping: Dict,
    ) -> None:
        """
        Заполняет все таблицы, переданные в команде:

        `python(3) manage.py db_fill --all`
        """
        for table in simple_model_mapping:
            fill_simple_and_foreign_key_tables(simple_model_mapping, table)

        for m2m_table in m2m_model_mapping:
            fill_many_to_many_tables(m2m_model_mapping, m2m_table)

    def fill_selected_tables(
        self, options: Dict,
        simple_model_mapping: Dict,
        m2m_model_mapping: dict,
    ) -> None:
        """Заполняет выбранные таблицы в команде."""

        for table in simple_model_mapping:
            if options.get(table, False):
                fill_simple_and_foreign_key_tables(simple_model_mapping, table)

        for m2m_table in m2m_model_mapping:
            if options.get(m2m_table, False):
                fill_many_to_many_tables(
                    m2m_model_mapping, m2m_table
                )
