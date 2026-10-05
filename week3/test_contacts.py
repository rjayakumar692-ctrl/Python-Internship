from contacts_manager import validate_phone, validate_email


def test_phone():
    print("Testing phone validation...")

    assert validate_phone("9876543210") == "9876543210"
    assert validate_phone("98765-43210") == "9876543210"
    assert validate_phone("12345") is None

    print("Phone tests passed.")


def test_email():
    print("Testing email validation...")

    assert validate_email("ravi@gmail.com") is True
    assert validate_email("test@example.com") is True
    assert validate_email("invalid-email") is False
    assert validate_email("") is True

    print("Email tests passed.")


if __name__ == "__main__":
    test_phone()
    test_email()

    print("\nAll tests passed successfully.")