"""
Модуль чтения файлов (CSV и JSON)
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Optional, Union

from app.core.core import DataFormatError


class CSVReader:
    """Класс для чтения CSV-файлов."""

    def read(self, file_path: Path) -> List[Dict]:
        """
        Считывает CSV-файл и возвращает список словарей
        """
        try:
            with file_path.open("r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                return list(reader)
        except Exception as exc:
            raise DataFormatError(
                f"Ошибка чтения CSV: {file_path.name}"
            ) from exc


class JSONReader:
    """Класс для чтения JSON файлов"""

    def read(self, file_path: Path) -> List[Dict]:
        """
        Считывает JSON файл и возвращает список словарей
        """
        try:
            with file_path.open("r", encoding="utf-8") as file:
                data = json.load(file)

            if not isinstance(data, list):
                raise DataFormatError("JSON должен содержать список")

            return data

        except Exception as exc:
            raise DataFormatError(
                f"Ошибка чтения JSON: {file_path.name}"
            ) from exc


def get_reader(file_path: Path) -> Optional[Union[CSVReader, JSONReader]]:
    """
    Возвращает подходящий ридер в зависимости от расширения файла
    """
    if file_path.suffix == ".csv":
        return CSVReader()
    if file_path.suffix == ".json":
        return JSONReader()
    return None
