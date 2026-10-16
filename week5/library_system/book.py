from datetime import datetime, timedelta


class Book:
    """Represents a book in the library."""

    def __init__(self, title, author, isbn, year=None):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.year = year
        self.available = True
        self.borrowed_by = None
        self.due_date = None
        self.date_added = datetime.now().strftime("%Y-%m-%d")

    def check_out(self, member_id, loan_period=14):
        """Check out the book to a member."""

        if not self.available:
            return False, "Book is already checked out."

        self.available = False
        self.borrowed_by = member_id

        due_date = datetime.now() + timedelta(days=loan_period)
        self.due_date = due_date.strftime("%Y-%m-%d")

        return True, f"Book checked out successfully. Due date: {self.due_date}"

    def return_book(self):
        """Return the book to the library."""

        if self.available:
            return False, "Book is already available."

        overdue = self.is_overdue()

        self.available = True
        self.borrowed_by = None
        self.due_date = None

        if overdue:
            return True, "Book returned successfully. It was overdue."

        return True, "Book returned successfully."

    def is_overdue(self):
        """Check whether the book is overdue."""

        if self.available or not self.due_date:
            return False

        due_date = datetime.strptime(self.due_date, "%Y-%m-%d")
        return datetime.now() > due_date

    def days_overdue(self):
        """Return number of overdue days."""

        if not self.is_overdue():
            return 0

        due_date = datetime.strptime(self.due_date, "%Y-%m-%d")
        return (datetime.now() - due_date).days

    def to_dict(self):
        """Convert book object into dictionary."""

        return {
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "year": self.year,
            "available": self.available,
            "borrowed_by": self.borrowed_by,
            "due_date": self.due_date,
            "date_added": self.date_added
        }

    @classmethod
    def from_dict(cls, data):
        """Create Book object from dictionary."""

        book = cls(
            data["title"],
            data["author"],
            data["isbn"],
            data.get("year")
        )

        book.available = data.get("available", True)
        book.borrowed_by = data.get("borrowed_by")
        book.due_date = data.get("due_date")
        book.date_added = data.get(
            "date_added",
            datetime.now().strftime("%Y-%m-%d")
        )

        return book

    def __str__(self):
        if self.available:
            status = "Available"
        else:
            status = f"Borrowed by {self.borrowed_by}"

        return (
            f"{self.title} by {self.author} "
            f"({self.isbn}) - {status}"
        )