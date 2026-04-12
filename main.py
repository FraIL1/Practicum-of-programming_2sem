"""
Точка входа в приложение
"""

import json
import logging
from pathlib import Path
from typing import List, Dict

from app.core.core import BaseAppError
from app.io.readers import get_reader
from app.services.services import validate_record, Aggregator

# Настройка логирования
logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8",
)


def save_result(data: Dict) -> None:
    tmp = Path("result.json.tmp")
    final = Path("result.json")

    try:
        with tmp.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        tmp.replace(final)

    except OSError as exc:
        logging.error(f"Ошибка записи файла: {exc}")


def print_report(total: int, success: int, errors: List[str]) -> None:
    """
    Выводит итоговый отчёт в консоль
    """
    print(f"Обработано: {total}")
    print(f"Успешно: {success}")
    print(f"Ошибок: {len(errors)}")

    if errors:
        print("Список ошибок:")
        for err in errors:
            print(f"- {err}")


def main() -> None:
    """
    Основная логика работы приложения
    """
    data_dir = Path("data")

    if not data_dir.exists():
        logging.critical("Папка data не найдена")
        raise SystemExit(1)

    aggregator = Aggregator()
    errors: List[str] = []

    total_files = 0
    success_files = 0

    for file_path in data_dir.iterdir():
        if not file_path.is_file():
            continue

        total_files += 1
        reader = get_reader(file_path)

        if reader is None:
            msg = f"Неподдерживаемый файл: {file_path.name}"
            logging.warning(msg)
            errors.append(msg)
            continue

        try:
            records = reader.read(file_path)
            valid_found = False

            for record in records:
                try:
                    transaction = validate_record(record)
                    aggregator.add(transaction)
                    valid_found = True
                except BaseAppError as exc:
                    logging.warning(f"{file_path.name}: {exc}")
                    errors.append(f"{file_path.name}: {exc}")

            if valid_found:
                success_files += 1

        except BaseAppError as exc:
            logging.error(f"{file_path.name}: {exc}")
            errors.append(f"{file_path.name}: {exc}")

    save_result(aggregator.result())
    print_report(total_files, success_files, errors)


if __name__ == "__main__":
    main()
