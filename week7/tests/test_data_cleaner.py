
import pandas as pd

from sales_analyzer.data_cleaner import SalesDataCleaner


def sample_data():
    return pd.DataFrame({
        "order_id": [1, 2, 2],
        "order_date": ["2024-01-10", "2024-02-15", "2024-02-15"],
        "customer_id": ["C1", "C2", "C2"],
        "product_id": ["P1", "P2", "P2"],
        "product_name": ["Pen", "Book", "Book"],
        "category": ["Stationery", "Books", "Books"],
        "quantity": [2, 3, 3],
        "unit_price": [10, 20, 20],
        "total_amount": [20, 60, 60],
        "region": ["North", "South", "South"],
    })


def test_duplicates_are_removed():
    cleaned = SalesDataCleaner().clean_data(sample_data())

    assert len(cleaned) == 2


def test_date_and_month_columns_are_created():
    cleaned = SalesDataCleaner().clean_data(sample_data())

    assert pd.api.types.is_datetime64_any_dtype(cleaned["order_date"])
    assert "month_year" in cleaned.columns
    assert cleaned.loc[0, "month_year"] == "2024-01"


def test_total_amount_is_calculated():
    cleaned = SalesDataCleaner().clean_data(sample_data())

    first = cleaned.loc[cleaned["order_id"] == 1].iloc[0]
    assert first["total_amount"] == 20
