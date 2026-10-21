from library_system.member import Member


def test_member_creation():
    member = Member("Jayakumar", "MEM001")

    assert member.name == "Jayakumar"
    assert member.member_id == "MEM001"
    assert member.borrowed_books == []


def test_member_borrow_book():
    member = Member("Jayakumar", "MEM001")

    success, message = member.borrow_book("ISBN001")

    assert success is True
    assert "ISBN001" in member.borrowed_books


def test_member_return_book():
    member = Member("Jayakumar", "MEM001")

    member.borrow_book("ISBN001")

    success, message = member.return_book("ISBN001")

    assert success is True
    assert "ISBN001" not in member.borrowed_books