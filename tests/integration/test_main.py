import pytest
import json
from pathlib import Path
from unittest.mock import patch
import main


class TestMain:
    def test_main_successful_flow(self, tmp_path, monkeypatch):
        """Тест успешного выполнения main.py"""
        # Создаем структуру data с валидными файлами
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Создаем валидный CSV
        (data_dir / "valid.csv").write_text(
            "id,amount,category,date\n1,100,Food,2024-01-01\n2,200,Taxi,2024-01-02"
        )
        
        # ВАЖНО: меняем текущую директорию на tmp_path
        monkeypatch.chdir(tmp_path)
        
        # Запускаем main
        with patch('builtins.print') as mock_print:
            main.main()
        
        # Проверяем, что result.json создался
        result_file = tmp_path / "result.json"
        assert result_file.exists()
        
        # Проверяем содержимое
        data = json.loads(result_file.read_text())
        # Теперь должно быть не пусто
        assert data != {}
        # Или проверяем конкретные категории
        if "Food" in data:
            assert data["Food"] == 100.0
        if "Taxi" in data:
            assert data["Taxi"] == 200.0
    
    def test_main_no_data_folder(self, tmp_path, monkeypatch):
        """Тест: папка data отсутствует"""
        monkeypatch.chdir(tmp_path)
        
        with pytest.raises(SystemExit):
            main.main()
    
    def test_main_with_invalid_files(self, tmp_path, monkeypatch):
        """Тест: смесь валидных и невалидных файлов"""
        data_dir = tmp_path / "data"
        data_dir.mkdir()
        
        # Валидный файл
        (data_dir / "good.csv").write_text(
            "id,amount,category,date\n1,100,Food,2024-01-01"
        )
        # Невалидный файл (отрицательная сумма)
        (data_dir / "bad.csv").write_text(
            "id,amount,category,date\n2,-50,Test,2024-01-01"
        )
        # Неподдерживаемый файл
        (data_dir / "bad.txt").write_text("text")
        
        monkeypatch.chdir(tmp_path)
        
        with patch('builtins.print') as mock_print:
            main.main()
        
        # Проверяем, что программа не упала
        result_file = tmp_path / "result.json"
        assert result_file.exists()
        
        # Только валидная транзакция должна быть в результате
        data = json.loads(result_file.read_text())
        assert data == {"Food": 100.0}