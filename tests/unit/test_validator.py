import pytest
from app.services.services import validate_record
from app.core.core import InvalidTransactionError


@pytest.mark.parametrize(
    "amount, is_valid",
    [
        ("100", True),
        ("0.01", True),
        ("0", False),
        ("-1", False),
        ("abc", False),
        (None, False),
        ("999999999999999999999", True),
        ("", False),
        (" ", False),
        ("50.123", True),
        ("-0.0001", False),
    ],
)
def test_validate_amount(amount, is_valid):
    record = {
        "id": "1",
        "amount": amount,
        "category": "test",
        "date": "2024-01-01",
    }

    if is_valid:
        result = validate_record(record)
        assert result.amount > 0
    else:
        with pytest.raises(InvalidTransactionError):
            validate_record(record)


def test_missing_fields(invalid_record_missing_field):
    with pytest.raises(InvalidTransactionError):
        validate_record(invalid_record_missing_field)


def test_not_dict():
    with pytest.raises(InvalidTransactionError):
        validate_record(["not", "a", "dict"])
