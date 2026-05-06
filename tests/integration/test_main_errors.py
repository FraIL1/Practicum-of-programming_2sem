"""
Тесты для проверки обработки ошибок в main()
Проверяет: отсутствие папки data, некорректные файлы
"""

import pytest
from main import main


def test_no_data_folder(tmp_path, monkeypatch):
    """Если папка data отсутствует, программа завершается с ошибкой"""
    monkeypatch.chdir(tmp_path)  # Переключаемся во временную пустую папку

    with pytest.raises(SystemExit):  # main() должен вызвать sys.exit()
        main()
