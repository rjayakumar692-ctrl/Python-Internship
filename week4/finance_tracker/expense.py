from datetime import datetime


class Expense:
    VALID_CATEGORIES = [
        "Food",
        "Transport",
        "Shopping",
        "Bills",
        "Health",
        "Education",
        "Entertainment",
        "Other"
    ]

    def __init__(self, date, amount, category, description):
        self.date = self.validate_date(date)
        self.amount = self.validate_amount(amount)
        self.category = self.validate_category(category)
        self.description = self.validate_description(description)

    @staticmethod
    def validate_date(date):
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format.")

    @staticmethod
    def validate_amount(amount):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise ValueError("Amount must be a number.")

        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")

        return round(amount, 2)

    @classmethod
    def validate_category(cls, category):
        category = category.strip().title()

        if category not in cls.VALID_CATEGORIES:
            raise ValueError(
                f"Invalid category. Choose from: {', '.join(cls.VALID_CATEGORIES)}"
            )

        return category

    @staticmethod
    def validate_description(description):
        description = description.strip()

        if not description:
            raise ValueError("Description cannot be empty.")

        return description

    def to_dict(self):
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["date"],
            data["amount"],
            data["category"],
            data["description"]
        )

    def __str__(self):
        return (
            f"{self.date} | "
            f"₹{self.amount:.2f} | "
            f"{self.category} | "
            f"{self.description}"
        )