
from django.db.models import Model

from .exceptions import MappingError


class Data():
    """
    Простой класс для получения данных из маппинга таблиц.
    """

    def __init__(self, mapping: dict, table_name: str) -> None:
        self.mapping = mapping
        self.table_name = table_name
        self._validate_table()
        self.path = self.get_path()
        self.fields = self.get_fields()

    def _validate_table(self) -> None:
        if self.table_name not in self.mapping:
            raise MappingError(
                f'Таблица {self.table_name} не найдена в маппинге!'
            )

    def _get_mapping_config(self) -> dict:
        return self.mapping.get(self.table_name)

    def get_path(self) -> str:
        """Возвращает путь к файлу."""

        path = self._get_mapping_config().get('path')
        if path is None:
            raise MappingError(
                f'Проверьте маппинг таблицы {self.table_name}, путь не найден!'
            )
        return path

    def get_fields(self) -> dict:
        """Возвращает словарь из полей модели таблицы."""

        fields = self._get_mapping_config().get('fields')
        if fields is None:
            raise MappingError(
                f'Проверьте таблицу {self.table_name}, поля не найдены!'
            )
        return fields

    def get_simple_model(self) -> Model:
        """Возвращает модель, ответственную за таблицу."""

        model = self._get_mapping_config().get('model')
        if model is None:
            raise MappingError(
                f'Проверьте таблицу {self.table_name}, модель не найдена!'
            )
        return model


class M2MData(Data):
    """Класс для получения данных из маппинга таблиц M2M."""

    def get_m2m_models(self) -> tuple:
        """Возвращает кортеж из кортежей связанных моделей таблицы."""

        m2m_models = self._get_mapping_config().get('model')
        if m2m_models is None:
            raise MappingError(
                f'Проверьте таблицу {self.table_name}, модели M2M не найдены!'
            )
        return m2m_models

    def get_related_model_name(self) -> str:
        """Возвращает имя связанной модели."""

        related_model_name = self._get_mapping_config().get(
            'related_model_name'
        )
        if related_model_name is None:
            raise MappingError(
                f'Проверьте таблицу {self.table_name},'
                f'имя связанной модели не найдено!'
            )
        return related_model_name
