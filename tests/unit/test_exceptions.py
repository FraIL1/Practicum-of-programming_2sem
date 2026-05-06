"""
Тесты кастомных исключений
Проверка выбрасывания InvalidTransactionError при плохих данных
"""

import pytest
from app.services.services import validate_record
from app.core.core import InvalidTransactionError


def test_invalid_data_raises_validation_error():
    """Тест: запись с 'not_a_number' в amount вызывает ошибку валидации"""
    record = {
        "id": "1",
        "amount": "not_a_number",  # ← не число → ошибка!
        "category": "test",
        "date": "2024-01-01",
    }

    # Ожидаем, что validate_record выбросит кастомное исключение
    with pytest.raises(InvalidTransactionError):
        validate_record(record)
