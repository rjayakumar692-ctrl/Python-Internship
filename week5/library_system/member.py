class Member:
    """Represents a library member."""

    MAX_BOOKS = 5

    def __init__(self, name, member_id):
        self.name = name
        self.member_id = member_id
        self.borrowed_books = []

    def borrow_book(self, isbn):
        """Add a book to the member's borrowed books."""

        if len(self.borrowed_books) >= self.MAX_BOOKS:
            return False, "Borrowing limit reached. Maximum is 5 books."

        if isbn in self.borrowed_books:
            return False, "This book is already borrowed by the member."

        self.borrowed_books.append(isbn)

        return True, "Book added to member account."

    def return_book(self, isbn):
        """Remove a book from the member's borrowed books."""

        if isbn not in self.borrowed_books:
            return False, "This book is not borrowed by this member."

        self.borrowed_books.remove(isbn)

        return True, "Book removed from member account."

    def to_dict(self):
        """Convert member object into dictionary."""

        return {
            "name": self.name,
            "member_id": self.member_id,
            "borrowed_books": self.borrowed_books
        }

    @classmethod
    def from_dict(cls, data):
        """Create Member object from dictionary."""

        member = cls(
            data["name"],
            data["member_id"]
        )

        member.borrowed_books = data.get("borrowed_books", [])

        return member

    def __str__(self):
        return (
            f"{self.member_id} - {self.name} "
            f"(Books borrowed: {len(self.borrowed_books)})"
        )