from datetime import datetime


def get_valid_date(prompt):
    while True:
        date = input(prompt).strip()

        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Invalid date. Use YYYY-MM-DD.")


def get_positive_amount(prompt):
    while True:
        try:
            amount = float(input(prompt).strip())

            if amount <= 0:
                print("Amount must be greater than zero.")
                continue

            return amount

        except ValueError:
            print("Please enter a valid number.")


def get_valid_month():
    while True:
        try:
            month = int(input("Enter month (1-12): "))

            if 1 <= month <= 12:
                return month

            print("Month must be between 1 and 12.")

        except ValueError:
            print("Please enter a valid month.")


def get_valid_year():
    while True:
        try:
            year = int(input("Enter year: "))

            if 2000 <= year <= 2100:
                return year

            print("Enter a valid year.")

        except ValueError:
            print("Please enter a valid year.")