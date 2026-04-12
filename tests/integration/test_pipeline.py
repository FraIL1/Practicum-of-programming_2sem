import pytest
from unittest.mock import patch

from app.io.readers import CSVReader, JSONReader, get_reader
from app.services.services import validate_record, Aggregator
from app.core.core import DataFormatError, ValidationError


class TestFileReaders:
    """Интеграционные тесты для читателей файлов"""

    def test_csv_reader_integration(self, temp_csv_file):
        csv_content = (
            "id,amount,category,date\n"
            "1,100,Food,2026-01-01\n"   # good
            "2,-50,Bad,2026-01-01\n"   # bad
            "3,abc,Test,2026-01-01\n"  # bad
        )
        file_path = temp_csv_file(csv_content)

        reader = CSVReader()
        records = reader.read(file_path)

        aggregator = Aggregator()
        valid_count = 0

        for rec in records:
            try:
                tx = validate_record(rec)
                aggregator.add(tx)
                valid_count += 1
            except ValidationError:
                pass

        result = aggregator.result()

        assert valid_count == 1
        assert len(result) == 1
        assert result["Food"] == 100.0

    def test_json_reader_invalid_format(self, temp_json_file):
        """Проверка обработки невалидного JSON (объект вместо списка)"""
        content = '{"key": "value"}'
        file_path = temp_json_file(content)

        reader = JSONReader()
        with pytest.raises(DataFormatError):
            reader.read(file_path)

    def test_unsupported_extension(self, tmp_path):
        """Проверка работы фабрики ридеров с неизвестным расширением"""
        file_path = tmp_path / "data.xml"
        file_path.write_text("<xml></xml>")

        reader = get_reader(file_path)
        assert reader is None

    def test_save_result_creates_file(self, tmp_path):
        from main import save_result
        import json

        data = {"Food": 100.0}

        # меняем cwd
        import os
        old = os.getcwd()
        os.chdir(tmp_path)

        try:
            save_result(data)

            result_file = tmp_path / "result.json"
            assert result_file.exists()

            content = json.loads(result_file.read_text())
            assert content == data

        finally:
            os.chdir(old)

class TestErrorHandlingAndMocking:
    """Тесты на отказоустойчивость и моки"""

    @patch("pathlib.Path.open")
    @patch("logging.error")
    def test_disk_write_failure_mock(
        self, mock_log, mock_open_func, aggregator, valid_transaction_data
    ):
        mock_open_func.side_effect = OSError("Disk error")

        tx = validate_record(valid_transaction_data)
        aggregator.add(tx)

        from main import save_result

        # НЕ должно падать
        save_result(aggregator.result())

        assert mock_open_func.called
        assert mock_log.called

    def test_full_pipeline_with_tmp_path(self, tmp_path):
        """Сквозной тест: создание файлов -> обработка -> результат"""
        # 1. Подготовка (Arrange)
        data_dir = tmp_path / "data"
        data_dir.mkdir()

        # Хороший файл
        (data_dir / "good.csv").write_text(
            "id,amount,category,date\n1,500,Taxi,2026-01-01"
        )
        # Файл с дубликатом ID (твой код его просуммирует!)
        (data_dir / "dup.json").write_text(
            '[{"id": "1", "amount": "100", '
            '"category": "Taxi", "date": "2026-01-01"}]'
        )
        # Битый файл
        (data_dir / "bad.txt").write_text("not supported")

        # 2. Действие (Act) - эмулируем логику main.py
        aggregator = Aggregator()
        errors = []

        for f in data_dir.iterdir():
            if not f.is_file():
                continue
            reader = get_reader(f)
            if not reader:
                errors.append("Unsupported")
                continue

            try:
                records = reader.read(f)
                for rec in records:
                    try:
                        tx = validate_record(rec)
                        aggregator.add(tx)
                    except ValidationError:
                        errors.append("Validation Error")
            except Exception:
                errors.append("Read Error")

        # 3. Проверка (Assert)
        result = aggregator.result()
        assert "Taxi" in result
        # ВНИМАНИЕ: Твой код СУММИРУЕТ дубликаты! 500 + 100 = 600.
# Если бы была защита, было бы 500. Но тест проверяет РЕАЛЬНОСТЬ твоего кода.
        assert result["Taxi"] == 600.0
        assert "Unsupported" in errors
