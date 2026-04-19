from unittest.mock import patch
import logging
from main import save_result


def test_save_result_logs_error(caplog):
    with patch("pathlib.Path.open", side_effect=OSError("Disk error")):
        with caplog.at_level(logging.ERROR):
            save_result({"food": 100})

    assert "Ошибка записи файла" in caplog.text
