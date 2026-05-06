"""
Общие фикстуры для всех тестов (доступны без импорта)
Хранит: валидную запись, запись с пропущенным полем
"""
import pytest


@pytest.fixture
def valid_record():
    """Фикстура: эталонная валидная запись для тестов"""
    return {
        "id": "123",
        "amount": "100.5",
        "category": "food",
        "date": "2024-01-01",
    }


@pytest.fixture
def invalid_record_missing_field():
    """Фикстура: запись без поля date (для тестов ошибок)"""
    return {
        "id": "123",
        "amount": "100.5",
        "category": "food",
        # date отсутствует → ошибка!
    }
