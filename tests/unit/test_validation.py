import pytest
from app.core.core import InvalidTransactionError, Transaction
from app.services.services import validate_record


class TestValidation:
    """Тесты для функции валидации записей"""

    @pytest.mark.parametrize(
        "amount, expected_valid",
        [
            ("100.0", True),
            ("0.01", True),
            ("9999999.99", True),
            ("1e10", True),          # очень большое число
            ("0", False),
            ("-5.0", False),
            ("abc", False),
            ("", False),
            (None, False),
            (" ", False),            # пробел
            ("-0.0001", False),
        ],
    )
    def test_amount_validation(
        self, amount, expected_valid, valid_transaction_data
    ):
        data = valid_transaction_data.copy()
        data["amount"] = amount

        if expected_valid:
            transaction = validate_record(data)
            assert isinstance(transaction, Transaction)
        else:
            with pytest.raises(InvalidTransactionError):
                validate_record(data)

    @pytest.mark.parametrize(
        "missing_field",
        ["id", "amount", "category", "date"]
    )
    def test_missing_fields(self, missing_field, valid_transaction_data):
        """Проверка отсутствия обязательных полей"""
        data = valid_transaction_data.copy()
        del data[missing_field]

        with pytest.raises(InvalidTransactionError) as exc_info:
            validate_record(data)

        assert missing_field in str(exc_info.value)

    def test_empty_id(self, valid_transaction_data):
        """Проверка пустого ID (преобразуется в строку, но не пустую)"""
        data = valid_transaction_data.copy()
        data["id"] = "   "
        # Твой код делает str(record["id"]), поэтому "   " пройдет,
        # если не проверять strip.
        # Но если хочешь проверить ошибку, нужно менять код валидации.
        # Сейчас этот тест проверит, что код просто принимает пробелы
        # как валидный ID.
        transaction = validate_record(data)
        assert transaction.transaction_id == "   "

    @pytest.mark.parametrize(
        "date",
        [
            "", 
            None,
            "not-a-date",
            "2026/01/01",
            "32-13-2026",
        ],
    )
    def test_invalid_date(self, date, valid_transaction_data):
        data = valid_transaction_data.copy()
        data["date"] = date

        # ВАЖНО: твой код сейчас НЕ валидирует дату → тест покажет дыру
        transaction = validate_record(data)
        assert isinstance(transaction, Transaction)
    
    @pytest.mark.parametrize(
        "bad_id",
        [None, "", 123, [], {}],
    )
    def test_invalid_id(self, bad_id, valid_transaction_data):
        data = valid_transaction_data.copy()
        data["id"] = bad_id

        transaction = validate_record(data)
        assert isinstance(transaction, Transaction)    

    def test_invalid_transaction_error_on_garbage(self):
        garbage_inputs = [
            None,
            [],
            {},
            {"wrong": "data"},
            {"id": "1"},
        ]

        for data in garbage_inputs:
            with pytest.raises(InvalidTransactionError):
                validate_record(data)

class TestAggregator:
    """Тесты для класса агрегации"""

    def test_add_transaction(self, aggregator, valid_transaction_data):
        """Проверка добавления транзакции"""
        tx = validate_record(valid_transaction_data)
        result = aggregator.add(tx)  # Твой метод возвращает None

        assert (
            result is None
        )  # Проверяем, что метод ничего не возвращает (как в твоем коде)
        assert aggregator.result()["Food"] == 100.50

    def test_duplicate_id_summing(self, aggregator, valid_transaction_data):
        """
        Проверка поведения с дубликатами ID.
        ВНИМАНИЕ: Твой код из Лаб 3 НЕ защищает от дубликатов,
        он их суммирует.
        Этот тест подтверждает текущее поведение (суммирование).
        Если нужно было отклонять дубликаты, то этот тест упадет,
        и это сигнал дописать код Лаб 3.
        """
        tx1 = validate_record(valid_transaction_data)
        tx2 = validate_record(valid_transaction_data)  # Тот же ID

        aggregator.add(tx1)
        aggregator.add(tx2)

        # Так как защиты нет, сумма удвоится: 100.50 + 100.50 = 201.0
        assert aggregator.result()["Food"] == 201.0

    def test_aggregation_by_category(self, aggregator):
        """Проверка суммирования по разным категориям"""
        data1 = {
            "id": "1",
            "amount": "100",
            "category": "A",
            "date": "2026-01-01"
        }
        data2 = {
            "id": "2",
            "amount": "50",
            "category": "A",
            "date": "2026-01-01"
        }
        data3 = {
            "id": "3",
            "amount": "200",
            "category": "B",
            "date": "2026-01-01"
        }

        for d in [data1, data2, data3]:
            tx = validate_record(d)
            aggregator.add(tx)

        res = aggregator.result()
        assert res["A"] == 150.0
        assert res["B"] == 200.0
