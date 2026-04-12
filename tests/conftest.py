import pytest
from app.services.services import Aggregator


@pytest.fixture
def valid_transaction_data():
    """
    Возвращает ШАБЛОН данных (словарь), так как validate_record принимает dict.
    """
    return {
        "id": "tx_001",
        "amount": "100.50",
        "category": "Food",
        "date": "2026-03-01",
    }


@pytest.fixture
def aggregator():
    """Чистый агрегатор для каждого теста"""
    return Aggregator()


@pytest.fixture
def temp_csv_file(tmp_path):
    """Создает временный CSV файл с заданным содержимым"""

    def _create_csv(content: str):
        file_path = tmp_path / "test_data.csv"
        file_path.write_text(content, encoding="utf-8")
        return file_path

    return _create_csv


@pytest.fixture
def temp_json_file(tmp_path):
    """Создает временный JSON файл с заданным содержимым"""

    def _create_json(content: str):
        file_path = tmp_path / "test_data.json"
        file_path.write_text(content, encoding="utf-8")
        return file_path

    return _create_json
