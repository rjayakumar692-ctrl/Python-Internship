import json
import csv
import re


# Store all contacts
contacts = {}


# -----------------------------
# Validation Functions
# -----------------------------

def validate_phone(phone):
    """Clean and validate a phone number."""

    phone = re.sub(r"\D", "", phone)

    if 10 <= len(phone) <= 15:
        return phone

    return None


def validate_email(email):
    """Validate email address."""

    if email == "":
        return True

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    return re.match(pattern, email) is not None


# -----------------------------
# File Handling Functions
# -----------------------------

def save_contacts():
    """Save contacts to JSON file."""

    with open("contacts_data.json", "w") as file:
        json.dump(contacts, file, indent=4)

    print("Contacts saved successfully.")


def load_contacts():
    """Load contacts from JSON file."""

    global contacts

    try:
        with open("contacts_data.json", "r") as file:
            contacts = json.load(file)

    except FileNotFoundError:
        contacts = {}

    except json.JSONDecodeError:
        contacts = {}


# -----------------------------
# Contact Functions
# -----------------------------

def add_contact():
    """Add a new contact."""

    name = input("Enter name: ").strip()

    if name == "":
        print("Name cannot be empty.")
        return

    phone = input("Enter phone number: ").strip()

    phone = validate_phone(phone)

    if phone is None:
        print("Invalid phone number.")
        return

    email = input("Enter email (optional): ").strip()

    if not validate_email(email):
        print("Invalid email address.")
        return

    key = name.lower()

    if key in contacts:
        print("Contact already exists.")
        return

    contacts[key] = {
        "name": name,
        "phone": phone,
        "email": email
    }

    save_contacts()

    print("Contact added successfully.")


def search_contact():
    """Search contacts using part of the name."""

    search = input("Enter name to search: ").strip().lower()

    found = False

    for contact in contacts.values():

        if search in contact["name"].lower():

            print("\nContact Found")
            print("----------------")
            print("Name :", contact["name"])
            print("Phone:", contact["phone"])
            print("Email:", contact["email"])

            found = True

    if not found:
        print("No contacts found.")


def display_all():
    """Display all contacts."""

    if not contacts:
        print("No contacts available.")
        return

    print("\nAll Contacts")
    print("----------------")

    for contact in contacts.values():

        print("Name :", contact["name"])
        print("Phone:", contact["phone"])
        print("Email:", contact["email"])
        print("----------------")


def update_contact():
    """Update an existing contact."""

    name = input("Enter contact name to update: ").strip().lower()

    if name not in contacts:
        print("Contact not found.")
        return

    contact = contacts[name]

    print("\nLeave a field empty to keep the existing value.")

    new_phone = input(
        f"Enter new phone [{contact['phone']}]: "
    ).strip()

    if new_phone != "":
        new_phone = validate_phone(new_phone)

        if new_phone is None:
            print("Invalid phone number.")
            return

        contact["phone"] = new_phone

    new_email = input(
        f"Enter new email [{contact['email']}]: "
    ).strip()

    if new_email != "":

        if not validate_email(new_email):
            print("Invalid email address.")
            return

        contact["email"] = new_email

    save_contacts()

    print("Contact updated successfully.")


def delete_contact():
    """Delete a contact."""

    name = input("Enter contact name to delete: ").strip().lower()

    if name not in contacts:
        print("Contact not found.")
        return

    del contacts[name]

    save_contacts()

    print("Contact deleted successfully.")


# -----------------------------
# CSV Export
# -----------------------------

def export_csv():
    """Export contacts to CSV file."""

    if not contacts:
        print("No contacts to export.")
        return

    with open("contacts.csv", "w", newline="") as file:

        writer = csv.writer(file)

        writer.writerow(["Name", "Phone", "Email"])

        for contact in contacts.values():

            writer.writerow([
                contact["name"],
                contact["phone"],
                contact["email"]
            ])

    print("Contacts exported to contacts.csv")


# -----------------------------
# Main Menu
# -----------------------------

def main():
    """Run the Contact Management System."""

    load_contacts()

    while True:

        print("\n===== Contact Management System =====")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Display All Contacts")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Export Contacts to CSV")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_contact()

        elif choice == "2":
            search_contact()

        elif choice == "3":
            display_all()

        elif choice == "4":
            update_contact()

        elif choice == "5":
            delete_contact()

        elif choice == "6":
            export_csv()

        elif choice == "7":
            print("Thank you for using Contact Management System.")
            break

        else:
            print("Invalid choice. Please try again.")


# Start the program
if __name__ == "__main__":
    main()