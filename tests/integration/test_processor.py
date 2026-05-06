"""
Тест связки: CSVReader → validate_record → Aggregator
Проверяет фильтрацию невалидных записей
"""

from app.io.readers import CSVReader
from app.services.services import validate_record, Aggregator


def test_csv_processing(tmp_path):
    """Обрабатываем CSV с плохими данными, получаем валидную сумму 100"""
    # Создаем тестовый CSV
    file_path = tmp_path / "test.csv"
    file_content = """id,amount,category,date
                        1,100,food,2024-01-01
                        2,-50,food,2024-01-01
                        3,abc,food,2024-01-01"""
    file_path.write_text(file_content, encoding="utf-8")

    # Читаем и обрабатываем
    reader = CSVReader()
    records = reader.read(file_path)

    aggregator = Aggregator()

    for record in records:
        try:
            transaction = validate_record(record)
            aggregator.add(transaction)
        except Exception:
            pass  # Пропускаем невалидные записи

    result = aggregator.result()

    # Проверяем: только 'food' с суммой 100
    assert len(result) == 1
    assert result["food"] == 100
