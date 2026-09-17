import pandas as pd
import pytest

from calculations import load_data


@pytest.fixture
def df():
    return load_data("data/sales-data.csv")


def test_load_data_returns_expected_shape_and_columns():
    result = load_data("data/sales-data.csv")
    assert len(result) == 482
    assert list(result.columns) == [
        "date", "order_id", "product", "category", "region",
        "quantity", "unit_price", "total_amount",
    ]


def test_load_data_parses_date_column_as_datetime():
    result = load_data("data/sales-data.csv")
    assert pd.api.types.is_datetime64_any_dtype(result["date"])


def test_load_data_raises_for_missing_file():
    with pytest.raises(FileNotFoundError):
        load_data("data/does-not-exist.csv")
