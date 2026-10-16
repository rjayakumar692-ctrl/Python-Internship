import json
import os
import shutil

from .book import Book
from .member import Member


class Library:
    """Manages books and members."""

    def __init__(self):
        self.books = {}
        self.members = {}

    # ---------------- BOOK MANAGEMENT ----------------

    def add_book(self, book):
        """Add a book to the library."""

        if book.isbn in self.books:
            return False, "A book with this ISBN already exists."

        self.books[book.isbn] = book

        return True, "Book added successfully."

    def remove_book(self, isbn):
        """Remove an available book."""

        if isbn not in self.books:
            return False, "Book not found."

        book = self.books[isbn]

        if not book.available:
            return False, "Cannot remove a borrowed book."

        del self.books[isbn]

        return True, "Book removed successfully."

    def find_book(self, isbn):
        """Find a book using ISBN."""

        return self.books.get(isbn)

    # ---------------- MEMBER MANAGEMENT ----------------

    def register_member(self, member):
        """Register a new member."""

        if member.member_id in self.members:
            return False, "Member ID already exists."

        self.members[member.member_id] = member

        return True, "Member registered successfully."

    def find_member(self, member_id):
        """Find a member using member ID."""

        return self.members.get(member_id)

    # ---------------- BORROW / RETURN ----------------

    def borrow_book(self, isbn, member_id):
        """Borrow a book for a member."""

        book = self.find_book(isbn)

        if not book:
            return False, "Book not found."

        member = self.find_member(member_id)

        if not member:
            return False, "Member not found."

        success, message = member.borrow_book(isbn)

        if not success:
            return False, message

        success, message = book.check_out(member_id)

        if not success:
            member.return_book(isbn)
            return False, message

        return True, message

    def return_book(self, isbn, member_id):
        """Return a borrowed book."""

        book = self.find_book(isbn)

        if not book:
            return False, "Book not found."

        member = self.find_member(member_id)

        if not member:
            return False, "Member not found."

        if book.borrowed_by != member_id:
            return False, "This book was not borrowed by this member."

        overdue_days = book.days_overdue()

        member.return_book(isbn)
        success, message = book.return_book()

        if not success:
            return False, message

        if overdue_days > 0:
            return True, (
                f"Book returned successfully. "
                f"Overdue by {overdue_days} day(s)."
            )

        return True, message

    # ---------------- SEARCH ----------------

    def search_books(self, keyword):
        """Search books by title, author, or ISBN."""

        keyword = keyword.lower()

        results = []

        for book in self.books.values():

            if (
                keyword in book.title.lower()
                or keyword in book.author.lower()
                or keyword in book.isbn.lower()
            ):
                results.append(book)

        return results

    def available_books(self):
        """Return all available books."""

        return [
            book for book in self.books.values()
            if book.available
        ]

    def overdue_books(self):
        """Return all overdue books."""

        return [
            book for book in self.books.values()
            if book.is_overdue()
        ]

    # ---------------- STATISTICS ----------------

    def statistics(self):
        """Return library statistics."""

        total_books = len(self.books)
        available = len(self.available_books())
        borrowed = total_books - available
        overdue = len(self.overdue_books())

        return {
            "total_books": total_books,
            "available_books": available,
            "borrowed_books": borrowed,
            "overdue_books": overdue,
            "total_members": len(self.members)
        }

    # ---------------- FILE OPERATIONS ----------------

    def save_data(self, books_file, members_file):
        """Save books and members to JSON files."""

        books_data = {
            isbn: book.to_dict()
            for isbn, book in self.books.items()
        }

        members_data = {
            member_id: member.to_dict()
            for member_id, member in self.members.items()
        }

        try:
            os.makedirs(os.path.dirname(books_file), exist_ok=True)
            os.makedirs(os.path.dirname(members_file), exist_ok=True)

            with open(books_file, "w", encoding="utf-8") as file:
                json.dump(books_data, file, indent=4)

            with open(members_file, "w", encoding="utf-8") as file:
                json.dump(members_data, file, indent=4)

            return True, "Data saved successfully."

        except OSError as error:
            return False, f"Error saving data: {error}"

    def load_data(self, books_file, members_file):
        """Load books and members from JSON files."""

        try:

            if os.path.exists(books_file):
                with open(books_file, "r", encoding="utf-8") as file:
                    books_data = json.load(file)

                self.books = {
                    isbn: Book.from_dict(data)
                    for isbn, data in books_data.items()
                }

            if os.path.exists(members_file):
                with open(members_file, "r", encoding="utf-8") as file:
                    members_data = json.load(file)

                self.members = {
                    member_id: Member.from_dict(data)
                    for member_id, data in members_data.items()
                }

            return True, "Data loaded successfully."

        except (OSError, json.JSONDecodeError) as error:
            return False, f"Error loading data: {error}"

    def create_backup(self, books_file, members_file, backup_dir):
        """Create backup copies of JSON files."""

        try:
            os.makedirs(backup_dir, exist_ok=True)

            if os.path.exists(books_file):
                shutil.copy2(
                    books_file,
                    os.path.join(backup_dir, "books_backup.json")
                )

            if os.path.exists(members_file):
                shutil.copy2(
                    members_file,
                    os.path.join(backup_dir, "members_backup.json")
                )

            return True, "Backup created successfully."

        except OSError as error:
            return False, f"Backup failed: {error}"