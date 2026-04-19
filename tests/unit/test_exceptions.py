import pytest
from app.services.services import validate_record
from app.core.core import InvalidTransactionError


def test_invalid_data_raises_validation_error():
    record = {
        "id": "1",
        "amount": "not_a_number",
        "category": "test",
        "date": "2024-01-01",
    }

    with pytest.raises(InvalidTransactionError):
        validate_record(record)
