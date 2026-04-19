import pytest


@pytest.fixture
def valid_record():
    return {
        "id": "123",
        "amount": "100.5",
        "category": "food",
        "date": "2024-01-01",
    }


@pytest.fixture
def invalid_record_missing_field():
    return {
        "id": "123",
        "amount": "100.5",
        "category": "food",
        # нет date
    }
