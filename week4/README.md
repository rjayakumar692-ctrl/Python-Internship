# Personal Finance Tracker

A Python-based Personal Finance Tracker that allows users to record, manage, search, analyze, and export their daily expenses. This project was developed as the Week 4 final project for a Python internship and demonstrates concepts such as object-oriented programming, file handling, data validation, exception handling, modular programming, testing, and reporting.

## Features

- Add new expenses
- View all recorded expenses
- Search expenses by category or description
- Filter expenses by category and month
- Support multiple expense categories
- Validate expense date, amount, category, and description
- Store expense data using JSON
- Export expense data to CSV
- Generate monthly expense reports
- View category-wise expense breakdown
- Display expense statistics
- Text-based expense visualization
- Set and update monthly budget
- Create data backups
- Restore data from backup
- Handle file and input errors
- Unit testing using pytest

## Technologies Used

- Python 3
- JSON
- CSV
- Object-Oriented Programming
- File Handling
- Exception Handling
- Pytest
- Git
- GitHub

## Project Structure

```text
week4-finance-tracker/
│
├── finance_tracker/
│   ├── __init__.py
│   ├── main.py
│   ├── expense.py
│   ├── expense_manager.py
│   ├── file_handler.py
│   ├── reports.py
│   └── utils.py
│
├── data/
│   ├── expenses.json
│   ├── backup/
│   └── exports/
│
├── tests/
│   ├── test_expense.py
│   ├── test_file_handler.py
│   └── test_reports.py
│
├── requirements.txt
├── README.md
├── .gitignore
└── run.py
```

## Module Description

### `expense.py`

Contains the `Expense` class.

It is responsible for:

- Creating expense objects
- Validating dates
- Validating amounts
- Validating categories
- Validating descriptions
- Converting expense objects to dictionaries
- Creating expense objects from saved data

### `expense_manager.py`

Contains the `ExpenseManager` class.

It manages the collection of expenses and provides functionality to:

- Add expenses
- Remove expenses
- Search expenses
- Filter by category
- Filter by month
- Calculate total expenses
- Calculate average expenses
- Find highest expense
- Find lowest expense

### `file_handler.py`

Handles data persistence and file operations.

It provides functionality for:

- Saving expenses to JSON
- Loading expenses from JSON
- Exporting expenses to CSV
- Creating backups
- Restoring backups
- Handling file-related errors

### `reports.py`

Generates expense reports and statistics.

It provides:

- Monthly summary reports
- Category-wise expense breakdown
- Total and average calculations
- Text-based category visualization

### `utils.py`

Contains reusable input validation functions for:

- Dates
- Amounts
- Months
- Years

### `main.py`

Contains the main `FinanceTracker` application and menu system.

It connects all the modules and provides the user interface.

### `run.py`

The entry point of the application.

The application can be started using:

```bash
python run.py
```

## Expense Categories

The application supports the following categories:

- Food
- Transport
- Shopping
- Bills
- Health
- Education
- Entertainment
- Other

## Data Storage

Expense data is stored in:

```text
data/expenses.json
```

Example:

```json
[
    {
        "date": "2026-10-12",
        "amount": 250.0,
        "category": "Food",
        "description": "Lunch"
    }
]
```

The application automatically loads previously saved expenses when it starts.

## CSV Export

Expense data can be exported to:

```text
data/exports/expenses.csv
```

The CSV file contains:

```text
date,amount,category,description
```

## Backup and Restore

The application supports data backup and restoration.

Backup files are stored in:

```text
data/backup/
```

The backup functionality helps prevent data loss and allows previously saved expense data to be restored.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/your-username/week4-finance-tracker.git
```

### 2. Open the project directory

```bash
cd week4-finance-tracker
```

### 3. Create a virtual environment

Windows:

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Application

Run the following command from the project root:

```bash
python run.py
```

The application displays a menu:

```text
============================================================
             PERSONAL FINANCE TRACKER
============================================================

========================================
              MAIN MENU
========================================
1. Add New Expense
2. View All Expenses
3. Search Expenses
4. Generate Monthly Report
5. View Category Breakdown
6. Set/Update Budget
7. Export Data to CSV
8. View Statistics
9. Backup/Restore Data
0. Exit
========================================
```

## Example

Adding an expense:

```text
Enter your choice (0-9): 1

--- ADD NEW EXPENSE ---

Enter date (YYYY-MM-DD): 2026-10-12
Enter amount: 250

Categories:
1. Food
2. Transport
3. Shopping
4. Bills
5. Health
6. Education
7. Entertainment
8. Other

Choose category: 1
Enter description: Lunch

Expense added successfully!
```

Viewing statistics:

```text
--- STATISTICS ---

Total expenses : 1
Total amount   : ₹250.00
Average expense: ₹250.00
Highest expense: ₹250.00 (Lunch)
Lowest expense : ₹250.00 (Lunch)
```

## Testing

The project uses `pytest` for unit testing.

Install pytest:

```bash
pip install pytest
```

Run all tests:

```bash
python -m pytest
```

The tests cover:

- Expense validation
- Invalid amounts
- Invalid dates
- Invalid categories
- JSON save and load operations
- Category breakdown
- Monthly reports

Example:

```text
========================= test session starts =========================

tests/test_expense.py ...
tests/test_file_handler.py ...
tests/test_reports.py ...

========================== 7 passed ==========================
```

## Error Handling

The application handles common errors such as:

- Invalid date format
- Invalid amount
- Negative amount
- Invalid category
- Empty description
- Missing JSON file
- Corrupted JSON file
- File permission errors
- Invalid menu choices
- Invalid month and year values

This prevents the application from crashing during normal user input.

## Learning Objectives

This project demonstrates practical understanding of:

- Python classes and objects
- Constructors
- Static methods and class methods
- Lists and dictionaries
- Functions
- Modules and packages
- JSON file handling
- CSV file handling
- Exception handling
- Input validation
- Searching and filtering
- Data analysis
- Basic reporting
- Unit testing
- Project organization
- Git and GitHub

## Future Enhancements

The following features can be added in future versions:

- CSV import
- Recurring expenses
- Advanced budget tracking
- Expense prediction based on historical data
- Graphical charts using Matplotlib
- Multiple user accounts
- Database integration using SQLite or MySQL
- Web-based interface
- Authentication and authorization

## Author

**Jayakumar Ravi**

Computer Science and Engineering Graduate

GitHub:  
https://github.com/rjayakumar692-ctrl

LinkedIn:  
https://linkedin.com/in/jayakumar692-jai