# Library Management System using Python OOP

## Project Overview

The Library Management System is a console-based Python application developed using Object-Oriented Programming (OOP) principles. It helps librarians manage books, register members, track borrowed books, process returns, search for books, calculate overdue periods, and maintain library records using JSON file storage.

This project was developed as part of my **Week 5 Self-Paced Python Internship** to strengthen my understanding of OOP, file handling, data persistence, and modular programming.

## Features

- **Book Management:** Add, view, search, and remove books.
- **Member Management:** Register members and track their borrowed books.
- **Borrow Books:** Issue available books to registered members with a 14-day loan period.
- **Return Books:** Return borrowed books and identify overdue returns.
- **Book Search:** Search by title, author, or ISBN.
- **Borrowing Limit:** Limit each member to a maximum of five borrowed books.
- **Overdue Tracking:** Identify overdue books and calculate the number of overdue days.
- **Library Statistics:** View total books, available books, borrowed books, overdue books, and registered members.
- **JSON Data Persistence:** Save and load book and member records using JSON files.
- **Backup Functionality:** Create backup copies of saved book and member records.
- **Input Validation:** Validate required fields, publication year, and menu choices.
- **Unit Testing:** Test application functionality using pytest.

## Technologies Used

- Python 3
- Object-Oriented Programming (OOP)
- JSON
- File Handling
- `datetime` and `timedelta`
- `os` and `shutil`
- pytest

## Project Structure

```text
week5/
├── library_system/
│   ├── __init__.py
│   ├── book.py
│   ├── member.py
│   ├── library.py
│   └── main.py
├── data/
│   ├── books.json
│   ├── members.json
│   └── backup/
├── tests/
│   ├── test_book.py
│   ├── test_member.py
│   └── test_library.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <your-github-repository-url>
cd week5
```

Replace `<your-github-repository-url>` with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

Run the following command from the project root directory:

```bash
python -m library_system.main
```

## How to Use

When the application starts, it displays a menu with the following options:

1. Add New Book
2. Register New Member
3. Borrow Book
4. Return Book
5. Search Books
6. View All Books
7. View All Members
8. View Overdue Books
9. View Statistics
10. Create Backup
11. Save & Exit
0. Exit Without Saving

Select the required option and follow the prompts displayed in the terminal.

## Data Storage

The application stores library records in JSON format:

- `data/books.json` — Stores book information, availability, borrower details, and due dates.
- `data/members.json` — Stores member information and borrowed book ISBNs.
- `data/backup/` — Stores backup copies of saved JSON records.

Choose **Save & Exit** to save the current records before closing the application.

## Running Tests

Install pytest if it is not already installed:

```bash
pip install pytest
```

Run the tests from the project root directory:

```bash
pytest
```

The tests cover book creation, borrowing and returning books, member management, and core library operations.

## OOP Concepts Demonstrated

- **Classes and Objects:** `Book`, `Member`, and `Library`.
- **Constructors:** Initialize objects using `__init__()`.
- **Instance Methods:** Implement book borrowing, returning, and member operations.
- **Class Methods:** Reconstruct objects from saved dictionaries using `from_dict()`.
- **Encapsulation:** Organize data and related behavior within classes.
- **Composition:** The `Library` class manages collections of books and members.
- **Modular Programming:** Separate responsibilities into multiple Python modules.

## Learning Outcomes

Through this project, I practiced designing classes, managing relationships between objects, handling JSON files, implementing search and validation, calculating overdue periods, creating backups, and writing unit tests.

## Future Improvements

- Add a graphical user interface.
- Implement late-return fines.
- Add book categories and filtering.
- Generate borrowing history reports.
- Improve data validation and recovery from corrupted files.

## Author

**Jayakumar Ravi**

Python Internship — Week 5 Project

GitHub: https://github.com/rjayakumar692-ctrl
