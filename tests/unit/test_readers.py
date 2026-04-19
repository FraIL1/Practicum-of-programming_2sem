import pytest

from app.io.readers import CSVReader, JSONReader
from app.core.core import DataFormatError


def test_csv_reader_success(tmp_path):
    file_path = tmp_path / "file.csv"
    file_path.write_text("id,amount,category,date\n1,100,food,2024-01-01")

    reader = CSVReader()
    data = reader.read(file_path)

    assert len(data) == 1


def test_json_reader_success(tmp_path):
    file_path = tmp_path / "file.json"
    file_path.write_text(
        '[{"id": "1", "amount": 100, "category": "food", "date": "2024"}]'
    )

    reader = JSONReader()
    data = reader.read(file_path)

    assert isinstance(data, list)


def test_json_invalid_format(tmp_path):
    file_path = tmp_path / "file.json"
    file_path.write_text('{"not": "a list"}')

    reader = JSONReader()

    with pytest.raises(DataFormatError):
        reader.read(file_path)


def test_get_reader_unknown_extension(tmp_path):
    from app.io.readers import get_reader

    file = tmp_path / "file.txt"
    file.write_text("test")

    assert get_reader(file) is None
