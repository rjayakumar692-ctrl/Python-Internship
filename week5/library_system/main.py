from .book import Book
from .member import Member
from .library import Library


BOOKS_FILE = "data/books.json"
MEMBERS_FILE = "data/members.json"
BACKUP_DIR = "data/backup"


def display_books(books):
    """Display books in a readable format."""

    if not books:
        print("\nNo books found.")
        return

    print("\n" + "-" * 60)

    for number, book in enumerate(books, start=1):

        print(f"{number}. {book.title}")
        print(f"   Author : {book.author}")
        print(f"   ISBN   : {book.isbn}")
        print(f"   Year   : {book.year}")

        if book.available:
            print("   Status : Available")
        else:
            print(f"   Status : Borrowed by {book.borrowed_by}")
            print(f"   Due    : {book.due_date}")

        print("-" * 60)


def add_book(library):
    """Add a new book."""

    print("\n--- Add New Book ---")

    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()
    isbn = input("Enter ISBN: ").strip()
    year = input("Enter publication year: ").strip()

    if not title or not author or not isbn:
        print("Title, author and ISBN are required.")
        return

    if year:
        if not year.isdigit():
            print("Year must be a number.")
            return

        year = int(year)

    else:
        year = None

    book = Book(title, author, isbn, year)

    success, message = library.add_book(book)

    print(message)


def register_member(library):
    """Register a new member."""

    print("\n--- Register Member ---")

    name = input("Enter member name: ").strip()
    member_id = input("Enter member ID: ").strip()

    if not name or not member_id:
        print("Name and member ID are required.")
        return

    member = Member(name, member_id)

    success, message = library.register_member(member)

    print(message)


def borrow_book(library):
    """Borrow a book."""

    print("\n--- Borrow Book ---")

    isbn = input("Enter ISBN: ").strip()
    member_id = input("Enter Member ID: ").strip()

    success, message = library.borrow_book(isbn, member_id)

    print(message)


def return_book(library):
    """Return a book."""

    print("\n--- Return Book ---")

    isbn = input("Enter ISBN: ").strip()
    member_id = input("Enter Member ID: ").strip()

    success, message = library.return_book(isbn, member_id)

    print(message)


def search_books(library):
    """Search books."""

    print("\n--- Search Books ---")

    keyword = input(
        "Enter title, author or ISBN to search: "
    ).strip()

    if not keyword:
        print("Search keyword cannot be empty.")
        return

    results = library.search_books(keyword)

    display_books(results)

    print(f"Found {len(results)} book(s).")


def view_members(library):
    """Display all members."""

    if not library.members:
        print("\nNo members registered.")
        return

    print("\n--- Library Members ---")

    for member in library.members.values():
        print(member)


def view_overdue_books(library):
    """Display overdue books."""

    overdue = library.overdue_books()

    print("\n--- Overdue Books ---")

    if not overdue:
        print("No overdue books.")
        return

    for book in overdue:
        print(f"\nTitle: {book.title}")
        print(f"ISBN: {book.isbn}")
        print(f"Borrowed By: {book.borrowed_by}")
        print(f"Due Date: {book.due_date}")
        print(f"Days Overdue: {book.days_overdue()}")


def show_statistics(library):
    """Display library statistics."""

    stats = library.statistics()

    print("\n--- Library Statistics ---")
    print(f"Total Books     : {stats['total_books']}")
    print(f"Available Books : {stats['available_books']}")
    print(f"Borrowed Books  : {stats['borrowed_books']}")
    print(f"Overdue Books   : {stats['overdue_books']}")
    print(f"Total Members   : {stats['total_members']}")


def show_menu():
    """Display main menu."""

    print("\n================================")
    print("     LIBRARY MANAGEMENT SYSTEM")
    print("================================")

    print("1. Add New Book")
    print("2. Register New Member")
    print("3. Borrow Book")
    print("4. Return Book")
    print("5. Search Books")
    print("6. View All Books")
    print("7. View All Members")
    print("8. View Overdue Books")
    print("9. View Statistics")
    print("10. Create Backup")
    print("11. Save & Exit")
    print("0. Exit Without Saving")


def main():
    library = Library()

    success, message = library.load_data(
        BOOKS_FILE,
        MEMBERS_FILE
    )

    print(message)

    while True:

        show_menu()

        choice = input("\nEnter your choice: ").strip()

        if choice == "1":
            add_book(library)

        elif choice == "2":
            register_member(library)

        elif choice == "3":
            borrow_book(library)

        elif choice == "4":
            return_book(library)

        elif choice == "5":
            search_books(library)

        elif choice == "6":
            display_books(list(library.books.values()))

        elif choice == "7":
            view_members(library)

        elif choice == "8":
            view_overdue_books(library)

        elif choice == "9":
            show_statistics(library)

        elif choice == "10":
            success, message = library.create_backup(
                BOOKS_FILE,
                MEMBERS_FILE,
                BACKUP_DIR
            )
            print(message)

        elif choice == "11":
            success, message = library.save_data(
                BOOKS_FILE,
                MEMBERS_FILE
            )

            print(message)

            if success:
                print("Thank you for using Library Management System.")
                break

        elif choice == "0":
            print("Exiting without saving.")
            break

        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()