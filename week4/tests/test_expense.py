import pytest

from finance_tracker.expense import Expense


def test_valid_expense():
    expense = Expense(
        "2026-10-12",
        500,
        "Food",
        "Lunch"
    )

    assert expense.amount == 500
    assert expense.category == "Food"


def test_invalid_amount():
    with pytest.raises(ValueError):
        Expense(
            "2026-10-12",
            -100,
            "Food",
            "Lunch"
        )


def test_invalid_date():
    with pytest.raises(ValueError):
        Expense(
            "12-10-2026",
            500,
            "Food",
            "Lunch"
        )


def test_invalid_category():
    with pytest.raises(ValueError):
        Expense(
            "2026-10-12",
            500,
            "Invalid",
            "Lunch"
        )