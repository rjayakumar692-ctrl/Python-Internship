# Student Grade Calculator

## Week 2 Project - Control Flow & Data Structures

## Project Description

The Student Grade Calculator is a beginner-level Python project developed as part of my Week 2 Python internship task.

The program accepts marks for multiple students in three subjects, calculates their average marks, determines their grade, provides a personalized comment, displays class statistics, and allows the user to search for a specific student.

This project helped me practice Python control flow, functions, lists, loops, input validation, and error handling.

---

## What I Learned

Through this project, I learned:

* How to use `if`, `elif`, and `else`
* How to create and use functions
* How to use `for` loops
* How to use `while` loops
* How to use `try-except` for error handling
* How to create and use lists
* How to use the `append()` method
* How to calculate averages
* How to use `sum()`, `len()`, `max()`, and `min()`
* How to format output using f-strings
* How to search for a student in a list
* How to organize a Python program into functions

---

## Features

The project includes:

* Accepts multiple students
* Accepts marks for three subjects
* Validates marks between 0 and 100
* Validates the number of students
* Handles invalid user input
* Calculates average marks
* Assigns grades based on average marks
* Provides personalized comments
* Stores student information using lists
* Displays results in a formatted table
* Calculates class average
* Finds the highest average
* Finds the lowest average
* Searches for a specific student

---

## Technologies Used

* Python 3
* Visual Studio Code
* Git
* GitHub

---

## How to Run

### Step 1: Install Python

Make sure Python 3 is installed.

Check the Python version using:

```bash
python --version
```

### Step 2: Open the Project

Open the `week2-grade-calculator` folder in Visual Studio Code.

### Step 3: Open the Terminal

Open the VS Code terminal.

### Step 4: Run the Program

Run:

```bash
python grade_calculator.py
```

### Step 5: Enter Student Information

The program will ask for:

* Number of students
* Student name
* Mathematics marks
* Science marks
* English marks

The program will calculate the average and grade automatically.

---

## Grading System

| Average Marks | Grade | Comment                            |
| ------------- | ----- | ---------------------------------- |
| 90 - 100      | A     | Excellent! Keep up the great work! |
| 80 - 89       | B     | Very Good! You're doing well.      |
| 70 - 79       | C     | Good. Room for improvement.        |
| 60 - 69       | D     | Needs Improvement.                 |
| Below 60      | F     | Needs significant improvement.     |

---

## Sample Output

```text
================================================================================
                         RESULTS
================================================================================
Name            Average    Grade    Comment
--------------------------------------------------------------------------------
Arun            87.67      B        Very Good! You're doing well.
Priya           75.00      C        Good. Room for improvement.
Rahul           94.67      A        Excellent! Keep up the great work.

==================================================
              CLASS STATISTICS
==================================================
Class Average : 85.78
Highest       : 94.67
Lowest        : 75.00

==================================================
                SEARCH STUDENT
==================================================
Enter a student name to search: Rahul

Student Found!
----------------------------------------
Name    : Rahul
Average : 94.67
Grade   : A
Comment : Excellent! Keep up the great work!
```

---

## Challenges and Solutions

### 1. Input Validation

**Challenge:**
The user may enter invalid marks such as text, negative numbers, or marks above 100.

**Solution:**
I used a `while` loop and `try-except` to validate the input.

---

### 2. Handling Multiple Students

**Challenge:**
The program needs to process information for multiple students.

**Solution:**
I used a `for` loop to process each student and lists to store their information.

---

### 3. Grade Calculation

**Challenge:**
Each student's grade needs to be calculated based on their average.

**Solution:**
I created a `calculate_grade()` function using `if`, `elif`, and `else`.

---

### 4. Calculating Class Statistics

**Challenge:**
I needed to find the class average, highest average, and lowest average.

**Solution:**
I stored the averages in a list and used `sum()`, `len()`, `max()`, and `min()`.

---

### 5. Searching for a Student

**Challenge:**
The program needs to find a particular student's result.

**Solution:**
I used a `for` loop to search the student names and used `.lower()` to make the search case-insensitive.

---

## Project Structure

```text
week2-grade-calculator/
│
├── grade_calculator.py
├── test_students.txt
├── results_sample.txt
├── README.md
└── .gitignore
```

---

## Conclusion

This project helped me understand the practical use of Python control flow and data structures.

I practiced conditions, functions, loops, lists, input validation, exception handling, calculations, and basic searching by developing a Student Grade Calculator.
