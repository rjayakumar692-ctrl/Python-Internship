from library_system.book import Book


def test_book_creation():
    book = Book(
        "Python Crash Course",
        "Eric Matthes",
        "ISBN001",
        2019
    )

    assert book.title == "Python Crash Course"
    assert book.author == "Eric Matthes"
    assert book.available is True


def test_book_checkout():
    book = Book(
        "Python Basics",
        "John Doe",
        "ISBN002"
    )

    success, message = book.check_out("MEM001")

    assert success is True
    assert book.available is False
    assert book.borrowed_by == "MEM001"
    assert book.due_date is not None


def test_book_return():
    book = Book(
        "Python Basics",
        "John Doe",
        "ISBN003"
    )

    book.check_out("MEM001")

    success, message = book.return_book()

    assert success is True
    assert book.available is True
    assert book.borrowed_by is None