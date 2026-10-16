from library_system.book import Book
from library_system.member import Member
from library_system.library import Library


def create_library():
    library = Library()

    book = Book(
        "Python Crash Course",
        "Eric Matthes",
        "ISBN001",
        2019
    )

    member = Member(
        "Jayakumar",
        "MEM001"
    )

    library.add_book(book)
    library.register_member(member)

    return library


def test_add_book():
    library = Library()

    book = Book(
        "Python Basics",
        "John Doe",
        "ISBN001"
    )

    success, message = library.add_book(book)

    assert success is True
    assert "ISBN001" in library.books


def test_register_member():
    library = Library()

    member = Member(
        "Jayakumar",
        "MEM001"
    )

    success, message = library.register_member(member)

    assert success is True
    assert "MEM001" in library.members


def test_borrow_book():
    library = create_library()

    success, message = library.borrow_book(
        "ISBN001",
        "MEM001"
    )

    assert success is True
    assert library.books["ISBN001"].available is False
    assert "ISBN001" in library.members["MEM001"].borrowed_books


def test_return_book():
    library = create_library()

    library.borrow_book(
        "ISBN001",
        "MEM001"
    )

    success, message = library.return_book(
        "ISBN001",
        "MEM001"
    )

    assert success is True
    assert library.books["ISBN001"].available is True