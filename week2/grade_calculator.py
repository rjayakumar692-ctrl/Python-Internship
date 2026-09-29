# ============================================================
# Student Grade Calculator
# Week 2 Project - Control Flow & Data Structures
# Author: Jayakumar Ravi
# ============================================================


# ------------------------------------------------------------
# 1. Calculate Grade and Comment
# ------------------------------------------------------------

def calculate_grade(average):
    """Calculate grade and comment based on average marks."""

    if average >= 90:
        return "A", "Excellent! Keep up the great work!"
    elif average >= 80:
        return "B", "Very Good! You're doing well."
    elif average >= 70:
        return "C", "Good. Room for improvement."
    elif average >= 60:
        return "D", "Needs Improvement."
    else:
        return "F", "Needs significant improvement."


# ------------------------------------------------------------
# 2. Get Valid Marks
# ------------------------------------------------------------

def get_marks(subject):
    """Get valid marks between 0 and 100."""

    while True:
        try:
            marks = float(input(f"{subject}: "))

            if 0 <= marks <= 100:
                return marks
            else:
                print("Please enter marks between 0 and 100.")

        except ValueError:
            print("Invalid input! Please enter a number.")


# ------------------------------------------------------------
# 3. Main Program
# ------------------------------------------------------------

def main():

    print("=" * 60)
    print("              STUDENT GRADE CALCULATOR")
    print("=" * 60)

    # --------------------------------------------------------
    # Get Number of Students
    # --------------------------------------------------------

    while True:
        try:
            num_students = int(input("Enter number of students: "))

            if num_students > 0:
                break
            else:
                print("Please enter a positive number.")

        except ValueError:
            print("Invalid input! Please enter a whole number.")


    # --------------------------------------------------------
    # Create Lists
    # --------------------------------------------------------

    student_names = []
    student_results = []


    # --------------------------------------------------------
    # Collect Student Information
    # --------------------------------------------------------

    for i in range(num_students):

        print(f"\n--- Student {i + 1} ---")

        # Get student name
        name = input("Student name: ")

        while name.strip() == "":
            print("Name cannot be empty.")
            name = input("Student name: ")

        student_names.append(name)

        # Get marks
        print("Enter marks:")

        math = get_marks("Math")
        science = get_marks("Science")
        english = get_marks("English")

        # Calculate average
        average = (math + science + english) / 3

        # Calculate grade and comment
        grade, comment = calculate_grade(average)

        # Store result
        student_results.append([average, grade, comment])


    # --------------------------------------------------------
    # Display Results
    # --------------------------------------------------------

    print("\n" + "=" * 80)
    print("                         RESULTS")
    print("=" * 80)

    print(f"{'Name':<15} {'Average':<10} {'Grade':<8} Comment")
    print("-" * 80)

    for i in range(num_students):

        name = student_names[i]
        average = student_results[i][0]
        grade = student_results[i][1]
        comment = student_results[i][2]

        print(
            f"{name:<15} "
            f"{average:<10.2f} "
            f"{grade:<8} "
            f"{comment}"
        )


    # --------------------------------------------------------
    # Calculate Class Statistics
    # --------------------------------------------------------

    averages = []

    for result in student_results:
        averages.append(result[0])

    class_average = sum(averages) / len(averages)
    highest = max(averages)
    lowest = min(averages)

    print("\n" + "=" * 50)
    print("              CLASS STATISTICS")
    print("=" * 50)

    print(f"Class Average : {class_average:.2f}")
    print(f"Highest       : {highest:.2f}")
    print(f"Lowest        : {lowest:.2f}")


    # --------------------------------------------------------
    # Search for a Student
    # --------------------------------------------------------

    print("\n" + "=" * 50)
    print("                SEARCH STUDENT")
    print("=" * 50)

    search_name = input("Enter a student name to search: ")

    found = False

    for i in range(num_students):

        if student_names[i].lower() == search_name.lower():

            print("\nStudent Found!")
            print("-" * 40)

            print("Name    :", student_names[i])
            print("Average :", f"{student_results[i][0]:.2f}")
            print("Grade   :", student_results[i][1])
            print("Comment :", student_results[i][2])

            found = True
            break

    if not found:
        print("Student not found.")


    # --------------------------------------------------------
    # End Program
    # --------------------------------------------------------

    print("\n" + "=" * 60)
    print("Thank you for using the Grade Calculator!")
    print("=" * 60)


# ------------------------------------------------------------
# Start Program
# ------------------------------------------------------------

if __name__ == "__main__":
    main()