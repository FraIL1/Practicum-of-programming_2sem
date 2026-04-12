"""
Сервисный слой: валидация и агрегация данных
"""

from collections import defaultdict
from typing import Dict

from app.core.core import Transaction, ValidationError

# Обязательные поля записи
REQUIRED_FIELDS = {"id", "amount", "category", "date"}


def validate_record(record: Dict) -> Transaction:
    """
    Проверяет запись и преобразует её в объект Transaction

    Исключения:
        ValidationError — если данные некорректны
    """

    if not isinstance(record, dict):
        raise ValidationError("Запись должна быть словарем")

    missing = REQUIRED_FIELDS - record.keys()
    if missing:
        raise ValidationError(f"Отсутствуют поля: {missing}")

    try:
        amount = float(record["amount"])
    except (ValueError, TypeError):
        raise ValidationError("Поле amount должно быть числом")

    if amount <= 0:
        raise ValidationError("Поле amount должно быть больше 0")

    return Transaction(
        transaction_id=str(record["id"]),
        amount=amount,
        category=str(record["category"]),
        date=str(record["date"]),
    )


class Aggregator:
    """
    Класс для агрегации транзакций по категориям
    """

    def __init__(self) -> None:
        self._data: Dict[str, float] = defaultdict(float)

    def add(self, transaction: Transaction) -> None:
        """
        Добавляет транзакцию в агрегированные данные
        """
        self._data[transaction.category] += transaction.amount

    def result(self) -> Dict[str, float]:
        """
        Возвращает итоговую агрегацию
        """
        return dict(self._data)
