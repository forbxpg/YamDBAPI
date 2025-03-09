"""Логика обработки данных из csv-файлов и заполнения таблиц."""
import csv
from django.db.models import Model
from django.core.exceptions import ObjectDoesNotExist

from ..csv_config import BULK_CREATE_BATCH_SIZE
from .exceptions import FileDoesNotExist, FileFormatError, TableFillError
from .utils import Data, M2MData


def map_data(fields: dict, line: dict) -> dict:
    """
    Преобразует данные из csv-файла в словарь для заполнения модели.
    """
    mapped_data: dict = {}

    for field, value in fields.items():
        if isinstance(value, tuple):
            related_field_id, related_model = value
            try:
                mapped_data[field] = related_model.objects.get(
                    id=line.get(related_field_id)
                )
            except ObjectDoesNotExist as e:
                raise TableFillError(
                    f'Ошибка при заполнении таблицы {e}') from e
        else:
            mapped_data[field] = line.get(value)
    return mapped_data


def bulk_fill(
    model: Model, mapped_data_list: list, batch_size=BULK_CREATE_BATCH_SIZE
) -> None:
    """

    """

    batch = [model(**fields) for fields in mapped_data_list]
    model.objects.bulk_create(
        batch, batch_size=batch_size, ignore_conflicts=True
    )


def fill_simple_and_foreign_key_tables(mapping: dict, table_name: str) -> None:
    """
    Заполняет таблицы с простыми моделями и
    моделями, связанными через ForeignKey.
    """

    data = Data(mapping, table_name)

    try:
        with open(data.path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            mapped_data_list = []
            for line in reader:
                mapped_data_list.append(map_data(data.fields, line))
            if mapped_data_list:
                bulk_fill(data.get_simple_model(), mapped_data_list)
    except FileNotFoundError as e:
        raise FileDoesNotExist(
            f'Файл {table_name} не найден') from e
    except FileFormatError as e:
        raise FileFormatError(
            f'Ошибка при чтении файла {data.path}') from e
    except ObjectDoesNotExist as e:
        raise TableFillError(
            f'Ошибка при заполнении таблицы {e}') from e


def fill_many_to_many_tables(m2m_mapping: dict, table_name: str) -> None:
    """
      Заполняет таблицы с отношением многие ко многим.
    """

    data = M2MData(m2m_mapping, table_name)
    model = data.get_m2m_models()[0][1]
    related_model_name = data.get_related_model_name()
    getattr(model, related_model_name).through.objects.all().delete()

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
    except ObjectDoesNotExist as e:
        raise TableFillError(
            f'Ошибка при заполнении таблицы {e}') from e
    except FileNotFoundError as e:
        raise FileDoesNotExist(
            f'Файл {table_name} не найден') from e
    except FileFormatError as e:
        raise FileFormatError(
            f'Ошибка при чтении файла {data.path}') from e
