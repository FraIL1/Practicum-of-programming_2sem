"""
Сквозной тест полного pipeline от CSV до результата
Проверяет: чтение → валидацию → агрегацию → сохранение
"""

import json
from main import main


def test_full_pipeline(tmp_path, monkeypatch):
    # 1. Подготовка тестовых данных
    data_dir = tmp_path / "data"
    data_dir.mkdir()

    file = data_dir / "test.csv"
    file.write_text("""id,amount,category,date
            1,100,food,2024-01-01
            2,-50,food,2024-01-01
            3,abc,food,2024-01-01""")

    monkeypatch.chdir(tmp_path)  # Делаем временную папку текущей
    main()

    # 3. Проверка результата
    result_file = tmp_path / "result.json"
    data = json.loads(result_file.read_text())  # Читаем JSON

    assert data == {"food": 100}  # Только валидная сумма 100
