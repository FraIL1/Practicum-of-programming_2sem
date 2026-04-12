"""
Ядро приложения: модели данных и пользовательские исключения
"""

from dataclasses import dataclass


class BaseAppError(Exception):
    """Базовое исключение для всего приложения"""


class DataFormatError(BaseAppError):
    """Ошибка формата файла или невозможности его прочитать"""


class ValidationError(BaseAppError):
    """Ошибка бизнес-валидации данных"""


class CurrencyMismatchError(BaseAppError):
    """Ошибка несоответствия валют"""


@dataclass
class Transaction:
    """
    Представляет валидированную финансовую транзакцию
    """
    transaction_id: str
    amount: float
    category: str
    date: str


InvalidTransactionError = ValidationError
