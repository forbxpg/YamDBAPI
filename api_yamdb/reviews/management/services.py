"""Логика обработки данных из csv-файлов и заполнения таблиц."""

import csv
import logging
from typing import Dict, List, Tuple

from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist


from .csv_config import BULK_CREATE_BATCH_SIZE
from .exceptions import FileDoesNotExist, FileFormatError, TableFillError
from .utils import Data, M2MData


logger = logging.getLogger('import')


def map_data(fields: Dict, line: Dict) -> Dict:
    """
    Преобразует данные из csv-файла в словарь для создания объекта модели.

    Возвращает словарь, где ключи - это поля модели,
    а значения - данные из csv-файла.
    """
    mapped_data: Dict = {}

    for field, value in fields.items():
        if not isinstance(value, tuple):
            mapped_data[field] = line.get(value)
        else:
            related_field_id, related_model = value
            try:
                mapped_data[field] = related_model.objects.get(
                    id=line[related_field_id]
                )
            except ObjectDoesNotExist as e:
                error_msg = (
                    f'Связанный объект {related_model.__name__}'
                    f'{line.get(related_field_id)} не найден!'
                )
                logger.debug(error_msg)
                raise TableFillError(error_msg) from e
    return mapped_data


def bulk_fill(
        model: Model,
        mapped_data_list: List[Dict],
        batch_size: int = BULK_CREATE_BATCH_SIZE) -> None:
    """
    Заполняет таблицу данными из csv-файла.

    Использует bulk_create
    и заполняет таблицу пакетами по `BULK_CREATE_BATCH_SIZE` записей.
    """

    try:
        batch = [model(**fields) for fields in mapped_data_list]
        model.objects.bulk_create(
            batch, batch_size=batch_size, ignore_conflicts=True
        )
        logger.info(
            'Создано %d объектов модели %s', len(batch), model.__name__
        )
    except TableFillError as e:
        error_msg = f'Ошибка при заполнении таблицы {model.__name__}: {str(e)}'
        logger.exception(error_msg)
        raise TableFillError(
            f'Ошибка при заполнении таблицы {e}') from e


def fill_simple_and_foreign_key_tables(mapping: Dict, table_name: str) -> None:
    """
    Заполняет таблицы с простыми моделями и
    моделями, связанными через ForeignKey.
    """

    data = Data(mapping, table_name)

    try:
        logger.info('Попытка чтения csv-файла %s', data.path)
        with open(data.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            mapped_data_list = []
            for line in reader:
                mapped_data_list.append(map_data(data.fields, line))
            if mapped_data_list:
                bulk_fill(data.get_simple_model(), mapped_data_list)
        logger.info('Таблица %s заполнена', table_name)

    except FileNotFoundError as e:
        logger.debug('Файл %s не найден: %e', table_name, e)
        raise FileDoesNotExist(
            f'Файл {table_name} не найден') from e

    except FileFormatError as e:
        logger.debug('Ошибка при чтении файла %s: %e', data.path, e)
        raise FileFormatError(
            f'Ошибка при чтении файла {data.path}') from e

    except ObjectDoesNotExist as e:
        logger.debug('Ошибка при заполнении таблицы: %e', e)
        raise TableFillError(
            f'Ошибка при заполнении таблицы {e}') from e


def fill_many_to_many_tables(m2m_mapping: Dict, table_name: str) -> None:
    """
    Заполняет таблицы, связанные с помощью ManyToManyField.
    """

    data = M2MData(m2m_mapping, table_name)
    model = data.get_m2m_models()[0][1]
    related_model_name = data.get_related_model_name()
    getattr(model, related_model_name).through.objects.all().delete()
    logger.info('Таблица %s  предварительно очищена', table_name)

    try:
        with open(data.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for line in reader:
                models = data.get_m2m_models()
                (model_id, model), (related_model_id, related_model) = models

                model_object = model.objects.get(
                    id=line.get(model_id)
                )
                related_model_object = related_model.objects.get(
                    id=line.get(related_model_id)
                )
                related_objects = getattr(
                    model_object, data.get_related_model_name()
                )
                related_objects.add(related_model_object)
        logger.info('Таблица %s заполнена', table_name)

    except ObjectDoesNotExist as e:
        logger.info('Ошибка при заполнении таблицы: %e', e)
        raise TableFillError(
            f'Ошибка при заполнении таблицы {e}') from e

    except FileNotFoundError as e:
        logger.error('Файл %s не найден: %e', table_name, e)
        raise FileDoesNotExist(
            f'Файл {table_name} не найден') from e

    except FileFormatError as e:
        logger.error('Ошибка при чтении файла %s: %e', data.path, e)
        raise FileFormatError(
            f'Ошибка при чтении файла {data.path}') from e
