from datetime import datetime
from .expense import Expense


class ExpenseManager:

    def __init__(self, expenses=None):
        self.expenses = expenses if expenses else []

    def add_expense(self, expense):
        if not isinstance(expense, Expense):
            raise TypeError("Only Expense objects can be added.")

        self.expenses.append(expense)

    def remove_expense(self, index):
        if index < 0 or index >= len(self.expenses):
            raise IndexError("Invalid expense number.")

        return self.expenses.pop(index)

    def get_all_expenses(self):
        return self.expenses

    def search(self, keyword):
        keyword = keyword.lower().strip()

        return [
            expense
            for expense in self.expenses
            if keyword in expense.description.lower()
            or keyword in expense.category.lower()
        ]

    def filter_by_category(self, category):
        category = category.strip().title()

        return [
            expense
            for expense in self.expenses
            if expense.category == category
        ]

    def filter_by_month(self, year, month):
        return [
            expense
            for expense in self.expenses
            if datetime.strptime(expense.date, "%Y-%m-%d").year == year
            and datetime.strptime(expense.date, "%Y-%m-%d").month == month
        ]

    def get_total(self):
        return sum(expense.amount for expense in self.expenses)

    def get_average(self):
        if not self.expenses:
            return 0

        return self.get_total() / len(self.expenses)

    def get_highest(self):
        if not self.expenses:
            return None

        return max(self.expenses, key=lambda expense: expense.amount)

    def get_lowest(self):
        if not self.expenses:
            return None

        return min(self.expenses, key=lambda expense: expense.amount)