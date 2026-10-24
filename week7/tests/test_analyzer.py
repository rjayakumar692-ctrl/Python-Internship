
import pandas as pd

from sales_analyzer.analyzer import SalesAnalyzer


def sample_clean_data():
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "order_date": pd.to_datetime([
            "2024-01-10", "2024-01-15", "2024-02-05"
        ]),
        "customer_id": ["C1", "C2", "C1"],
        "product_id": ["P1", "P2", "P1"],
        "product_name": ["Pen", "Book", "Pen"],
        "category": ["Stationery", "Books", "Stationery"],
        "quantity": [2, 1, 3],
        "unit_price": [10, 50, 10],
        "total_amount": [20, 50, 30],
        "region": ["North", "South", "North"],
    })


def test_basic_statistics():
    analyzer = SalesAnalyzer(sample_clean_data())
    stats = analyzer.calculate_basic_stats()

    assert stats["total_revenue"] == 100
    assert stats["total_orders"] == 3
    assert stats["unique_customers"] == 2



def test_category_analysis():
    analyzer = SalesAnalyzer(sample_clean_data())
    categories = analyzer.sales_by_category()

    assert not categories.empty
    assert "category" in categories.columns
    assert "total_sales" in categories.columns
    assert categories["total_sales"].is_monotonic_decreasing



def test_monthly_sales():
    analyzer = SalesAnalyzer(sample_clean_data())
    monthly = analyzer.monthly_sales()

    assert len(monthly) == 2
    assert monthly.iloc[0]["month_year"] == "2024-01"
    assert monthly.iloc[0]["total_sales"] == 70


def test_top_products():
    analyzer = SalesAnalyzer(sample_clean_data())
    products = analyzer.top_products(1)

    assert products.iloc[0]["product_name"] == "Pen"
    assert products.iloc[0]["total_sales"] == 50


def test_forecast():
    analyzer = SalesAnalyzer(sample_clean_data())
    forecast = analyzer.monthly_sales_forecast(periods=2)

    assert len(forecast) == 2
    assert forecast.iloc[0]["month_year"] == "2024-03"
