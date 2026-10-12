from finance_tracker.expense import Expense
from finance_tracker.reports import Reports


def test_category_breakdown():
    expenses = [
        Expense("2026-10-01", 100, "Food", "Breakfast"),
        Expense("2026-10-02", 200, "Food", "Lunch"),
        Expense("2026-10-03", 300, "Transport", "Bus")
    ]

    breakdown = Reports.category_breakdown(expenses)

    assert breakdown["Food"] == 300
    assert breakdown["Transport"] == 300


def test_monthly_summary():
    expenses = [
        Expense("2026-10-01", 100, "Food", "Breakfast"),
        Expense("2026-10-05", 200, "Transport", "Bus"),
        Expense("2026-09-05", 500, "Bills", "Electricity")
    ]

    report = Reports.monthly_summary(
        expenses,
        2026,
        10
    )

    assert report["count"] == 2
    assert report["total"] == 300