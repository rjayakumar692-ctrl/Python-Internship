import csv
import json
import os

from .expense import Expense


class FileHandler:

    @staticmethod
    def ensure_directory(directory):
        os.makedirs(directory, exist_ok=True)

    @staticmethod
    def save_json(expenses, filename):
        try:
            directory = os.path.dirname(filename)

            if directory:
                FileHandler.ensure_directory(directory)

            data = [expense.to_dict() for expense in expenses]

            with open(filename, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)

            return True

        except PermissionError:
            print("Error: Permission denied while saving the file.")
            return False

        except OSError as error:
            print(f"Error saving file: {error}")
            return False

    @staticmethod
    def load_json(filename):
        try:
            if not os.path.exists(filename):
                return []

            with open(filename, "r", encoding="utf-8") as file:
                data = json.load(file)

            return [Expense.from_dict(item) for item in data]

        except json.JSONDecodeError:
            print("Error: JSON file is corrupted.")
            return []

        except PermissionError:
            print("Error: Permission denied while reading the file.")
            return []

        except OSError as error:
            print(f"Error reading file: {error}")
            return []

    @staticmethod
    def export_csv(expenses, filename):
        try:
            directory = os.path.dirname(filename)

            if directory:
                FileHandler.ensure_directory(directory)

            with open(filename, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(
                    file,
                    fieldnames=["date", "amount", "category", "description"]
                )

                writer.writeheader()

                for expense in expenses:
                    writer.writerow(expense.to_dict())

            return True

        except PermissionError:
            print("Error: Permission denied while exporting CSV.")
            return False

        except OSError as error:
            print(f"Error exporting CSV: {error}")
            return False

    @staticmethod
    def backup(filename, backup_filename):
        return FileHandler.save_json(
            FileHandler.load_json(filename),
            backup_filename
        )

    @staticmethod
    def restore(backup_filename, filename):
        expenses = FileHandler.load_json(backup_filename)

        if not expenses and os.path.exists(backup_filename):
            return False

        return FileHandler.save_json(expenses, filename)