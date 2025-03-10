"""Базовые исключения для команд."""


class FileDoesNotExist(Exception):
    """Исключение для несуществующего файла."""


class FileFormatError(Exception):
    """Исключение для некорректного формата файла."""


class TableFillError(Exception):
    """Исключение для ошибок заполнения таблиц."""


class MappingError(Exception):
    """Исключение для ошибок маппинга."""
