"""
Тесты для читателей файлов (CSVReader, JSONReader)
Проверяет: успешное чтение, обработку ошибок формата, определение чтения
"""

import pytest
from app.io.readers import CSVReader, JSONReader
from app.core.core import DataFormatError


def test_csv_reader_success(tmp_path):
    """CSVReader: успешно читает валидный CSV"""
    file_path = tmp_path / "file.csv"
    file_path.write_text("id,amount,category,date\n1,100,food,2024-01-01")

    reader = CSVReader()
    data = reader.read(file_path)

    assert len(data) == 1  # Прочитана 1 запись


def test_json_reader_success(tmp_path):
    """JSONReader: успешно читает валидный JSON (список объектов)"""
    file_path = tmp_path / "file.json"
    file_path.write_text(
        '[{"id": "1", "amount": 100, "category": "food", "date": "2024"}]'
    )

    reader = JSONReader()
    data = reader.read(file_path)

    assert isinstance(data, list)  # Должен вернуть список


def test_json_invalid_format(tmp_path):
    """JSONReader: файл с объектом вместо списка → ошибка формата"""
    file_path = tmp_path / "file.json"
    file_path.write_text('{"not": "a list"}')  # ← не список!

    reader = JSONReader()

    with pytest.raises(DataFormatError):  # Ожидаем ошибку
        reader.read(file_path)


def test_get_reader_unknown_extension(tmp_path):
    """get_reader(): .txt не поддерживается → возвращает None"""
    from app.io.readers import get_reader

    file = tmp_path / "file.txt"
    file.write_text("test")

    assert get_reader(file) is None  # Неизвестное расширение
