"""
Тест обработки ошибок при сохранении результата
Проверяет логирование при проблемах с записью файла
"""

from unittest.mock import patch
import logging
from main import save_result


def test_save_result_logs_error(caplog):
    """Тест: при ошибке диска save_result() логирует сообщение об ошибке"""
    # Мокаем open() так, чтобы он всегда выбрасывал ошибку диска
    with patch("pathlib.Path.open", side_effect=OSError("Disk error")):
        with caplog.at_level(logging.ERROR):  # Ловим логи уровня ERROR
            save_result({"food": 100})

    # Проверяем, что нужное сообщение попало в лог
    assert "Ошибка записи файла" in caplog.text
