# Contact Management System

A beginner-friendly Python project for managing contacts using dictionaries, functions, JSON, and CSV files.

## Features

* Add contacts
* Search contacts
* Display all contacts
* Update contacts
* Delete contacts
* Validate phone numbers
* Validate email addresses
* Save contacts using JSON
* Export contacts to CSV
* Basic testing

## Technologies Used

* Python
* Dictionaries
* Functions
* Loops
* Conditional statements
* String methods
* Regular expressions
* JSON
* CSV
* File handling

## Project Structure

```text
week3-contact-manager/
│
├── contacts_manager.py
├── contacts_data.json
├── test_contacts.py
├── README.md
├── requirements.txt
└── .gitignore
```

## How to Run

Open the project folder in the terminal.

Run:

```bash
python contacts_manager.py
```

The program will display a menu:

```text
===== Contact Management System =====
1. Add Contact
2. Search Contact
3. Display All Contacts
4. Update Contact
5. Delete Contact
6. Export Contacts to CSV
7. Exit
```

Choose an option by entering the corresponding number.

## Testing

Run:

```bash
python test_contacts.py
```

The test program checks phone number and email validation.

## Data Storage

Contacts are stored in:

```text
contacts_data.json
```

The program automatically loads contacts when it starts and saves changes to the JSON file.

## CSV Export

The "Export Contacts to CSV" option creates:

```text
contacts.csv
```

This file contains:

* Name
* Phone
* Email

## Learning Objectives

This project was created to practice:

* Python functions
* Dictionaries
* Loops
* Conditional statements
* Input validation
* String handling
* File handling
* JSON
* CSV
* Basic testing
* Error handling
