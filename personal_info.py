# Name: Jayakumar Ravi
# Project: Personal Information Manager
# Description: A simple Python program to store and display personal information.

# -------------------------------
# Static Personal Information
# -------------------------------

# Store the person's name
name = "Jayakumar Ravi"

# Store the person's age
age = 21

# Store the person's city
city = "Villupuram"

# Store the person's hobby
hobby = "Playing Cricket"


# -------------------------------
# Welcome Message
# -------------------------------

print("=" * 45)
print("     PERSONAL INFORMATION MANAGER")
print("=" * 45)
print("Welcome! Please enter your favorite things.\n")


# -------------------------------
# Get User Input
# -------------------------------

# Ask the user for their favorite food
favorite_food = input("Enter your favorite food: ").strip()

# Validate favorite food input
while not favorite_food:
    print("Favorite food cannot be empty.")
    favorite_food = input("Please enter your favorite food: ").strip()


# Ask the user for their favorite color
favorite_color = input("Enter your favorite color: ").strip()

# Validate favorite color input
while not favorite_color:
    print("Favorite color cannot be empty.")
    favorite_color = input("Please enter your favorite color: ").strip()


# -------------------------------
# Calculate Age in Months
# -------------------------------

age_in_months = age * 12


# -------------------------------
# Display Personal Information
# -------------------------------

print("\n" + "=" * 45)
print("          MY PERSONAL INFORMATION")
print("=" * 45)

print(f"Name          : {name.title()}")
print(f"Age           : {age} years")
print(f"Age in Months : {age_in_months} months")
print(f"City          : {city.title()}")
print(f"Hobby         : {hobby.title()}")

print("-" * 45)

print(f"Favorite Food : {favorite_food.title()}")
print(f"Favorite Color: {favorite_color.title()}")

print("=" * 45)


# -------------------------------
# Goodbye Message
# -------------------------------

print("Thank you for using the Personal Information Manager!")
print("Goodbye!")