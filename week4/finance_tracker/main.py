import os

from .expense import Expense
from .expense_manager import ExpenseManager
from .file_handler import FileHandler
from .reports import Reports
from .utils import (
    get_positive_amount,
    get_valid_date,
    get_valid_month,
    get_valid_year
)


DATA_FILE = "data/expenses.json"
BACKUP_FILE = "data/backup/expenses_backup.json"
CSV_FILE = "data/exports/expenses.csv"


class FinanceTracker:

    def __init__(self):
        expenses = FileHandler.load_json(DATA_FILE)
        self.manager = ExpenseManager(expenses)

    def save_data(self):
        FileHandler.save_json(
            self.manager.get_all_expenses(),
            DATA_FILE
        )

    def run(self):
        print("=" * 60)
        print("             PERSONAL FINANCE TRACKER")
        print("=" * 60)

        while True:
            self.display_menu()

            choice = input("\nEnter your choice (0-9): ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.view_expenses()
            elif choice == "3":
                self.search_expenses()
            elif choice == "4":
                self.generate_monthly_report()
            elif choice == "5":
                self.view_category_breakdown()
            elif choice == "6":
                self.set_budget()
            elif choice == "7":
                self.export_data()
            elif choice == "8":
                self.view_statistics()
            elif choice == "9":
                self.backup_restore()
            elif choice == "0":
                self.save_data()
                print("\nThank you for using Personal Finance Tracker!")
                break
            else:
                print("Invalid choice! Please enter 0-9.")

    @staticmethod
    def display_menu():
        print("\n" + "=" * 40)
        print("              MAIN MENU")
        print("=" * 40)
        print("1. Add New Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. Generate Monthly Report")
        print("5. View Category Breakdown")
        print("6. Set/Update Budget")
        print("7. Export Data to CSV")
        print("8. View Statistics")
        print("9. Backup/Restore Data")
        print("0. Exit")
        print("=" * 40)

    def add_expense(self):
        print("\n--- ADD NEW EXPENSE ---")

        try:
            date = get_valid_date("Enter date (YYYY-MM-DD): ")
            amount = get_positive_amount("Enter amount: ")

            print("\nCategories:")
            for index, category in enumerate(Expense.VALID_CATEGORIES, 1):
                print(f"{index}. {category}")

            category_choice = int(input("Choose category: "))

            if not 1 <= category_choice <= len(Expense.VALID_CATEGORIES):
                print("Invalid category.")
                return

            category = Expense.VALID_CATEGORIES[category_choice - 1]

            description = input("Enter description: ").strip()

            expense = Expense(
                date,
                amount,
                category,
                description
            )

            self.manager.add_expense(expense)
            self.save_data()

            print("Expense added successfully!")

        except (ValueError, TypeError) as error:
            print(f"Error: {error}")

    def view_expenses(self):
        print("\n--- ALL EXPENSES ---")

        expenses = self.manager.get_all_expenses()

        if not expenses:
            print("No expenses found.")
            return

        print("-" * 75)
        print(f"{'No.':<5}{'Date':<15}{'Amount':<15}{'Category':<18}Description")
        print("-" * 75)

        for index, expense in enumerate(expenses, 1):
            print(
                f"{index:<5}"
                f"{expense.date:<15}"
                f"₹{expense.amount:<14.2f}"
                f"{expense.category:<18}"
                f"{expense.description}"
            )

    def search_expenses(self):
        print("\n--- SEARCH EXPENSES ---")

        keyword = input("Enter keyword/category: ").strip()

        results = self.manager.search(keyword)

        if not results:
            print("No matching expenses found.")
            return

        for expense in results:
            print(expense)

    def generate_monthly_report(self):
        print("\n--- MONTHLY REPORT ---")

        year = get_valid_year()
        month = get_valid_month()

        Reports.display_monthly_report(
            self.manager.get_all_expenses(),
            year,
            month
        )

    def view_category_breakdown(self):
        Reports.display_category_chart(
            self.manager.get_all_expenses()
        )

    def set_budget(self):
        print("\n--- SET/UPDATE BUDGET ---")

        try:
            budget = get_positive_amount("Enter monthly budget: ")

            with open(
                "data/budget.txt",
                "w",
                encoding="utf-8"
            ) as file:
                file.write(str(budget))

            print(f"Monthly budget set to ₹{budget:.2f}")

        except OSError as error:
            print(f"Error saving budget: {error}")

    def export_data(self):
        print("\n--- EXPORT DATA ---")

        success = FileHandler.export_csv(
            self.manager.get_all_expenses(),
            CSV_FILE
        )

        if success:
            print(f"Data exported successfully to {CSV_FILE}")

    def view_statistics(self):
        print("\n--- STATISTICS ---")

        manager = self.manager

        print(f"Total expenses : {len(manager.expenses)}")
        print(f"Total amount   : ₹{manager.get_total():.2f}")
        print(f"Average expense: ₹{manager.get_average():.2f}")

        highest = manager.get_highest()
        lowest = manager.get_lowest()

        if highest:
            print(f"Highest expense: ₹{highest.amount:.2f} ({highest.description})")

        if lowest:
            print(f"Lowest expense : ₹{lowest.amount:.2f} ({lowest.description})")

    def backup_restore(self):
        print("\n--- BACKUP/RESTORE ---")
        print("1. Create Backup")
        print("2. Restore Backup")
        print("3. Cancel")

        choice = input("Choose option: ").strip()

        if choice == "1":
            success = FileHandler.backup(
                DATA_FILE,
                BACKUP_FILE
            )

            if success:
                print("Backup created successfully.")

        elif choice == "2":
            if not os.path.exists(BACKUP_FILE):
                print("No backup file found.")
                return

            success = FileHandler.restore(
                BACKUP_FILE,
                DATA_FILE
            )

            if success:
                self.manager = ExpenseManager(
                    FileHandler.load_json(DATA_FILE)
                )
                print("Data restored successfully.")
            else:
                print("Unable to restore backup.")

        elif choice == "3":
            print("Cancelled.")

        else:
            print("Invalid choice.")


def main():
    tracker = FinanceTracker()
    tracker.run()


if __name__ == "__main__":
    main()