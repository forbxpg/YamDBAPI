"""Настройка логгера."""
import logging
import sys


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
formatter = logging.Formatter(
    '[%(asctime)s] | %(name)s - %(levelname)s - %(message)s {%(funcName)s()}'
)
handler.setFormatter(formatter)
logger.addHandler(handler)
