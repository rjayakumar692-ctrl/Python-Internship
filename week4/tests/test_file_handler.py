from finance_tracker.expense import Expense
from finance_tracker.file_handler import FileHandler


def test_json_save_and_load(tmp_path):
    file_path = tmp_path / "expenses.json"

    expense = Expense(
        "2026-10-12",
        500,
        "Food",
        "Lunch"
    )

    FileHandler.save_json([expense], str(file_path))

    expenses = FileHandler.load_json(str(file_path))

    assert len(expenses) == 1
    assert expenses[0].amount == 500
    assert expenses[0].category == "Food"