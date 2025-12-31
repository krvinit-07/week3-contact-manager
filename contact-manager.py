# Contact Management System
# Week 3 Project – Functions & Dictionaries
# Author: Vinit Kumar

import json
import re
import csv
from datetime import datetime

DATA_FILE = "contacts_data.json"


# --------------------------------------------------
# Utility / Validation Functions
# --------------------------------------------------

def clean_phone(phone):
    """
    Removes non-digit characters and validates length.
    Returns cleaned phone number or None.
    """
    digits = re.sub(r"\D", "", phone)
    if 10 <= len(digits) <= 15:
        return digits
    return None


def validate_email(email):
    """
    Validates email format using regex.
    """
    if not email:
        return True
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w{2,}$'
    return re.match(pattern, email) is not None


# --------------------------------------------------
# File Handling Functions
# --------------------------------------------------

def load_contacts():
    """
    Load contacts from JSON file if exists.
    """
    try:
        with open(DATA_FILE, "r") as file:
            print("✔ Contacts loaded successfully.")
            return json.load(file)
    except FileNotFoundError:
        print("✔ No existing contacts file found. Starting fresh.")
        return {}


def save_contacts(contacts):
    """
    Save contacts dictionary to JSON file.
    """
    with open(DATA_FILE, "w") as file:
        json.dump(contacts, file, indent=4)
    print("✔ Contacts saved successfully.")


# --------------------------------------------------
# CRUD Operations
# --------------------------------------------------

def add_contact(contacts):
    print("\n--- ADD NEW CONTACT ---")

    name = input("Enter contact name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    if name in contacts:
        print(f"Contact '{name}' already exists.")
        return

    phone = input("Enter phone number: ").strip()
    phone = clean_phone(phone)
    if not phone:
        print("Invalid phone number.")
        return

    email = input("Enter email (optional): ").strip()
    if not validate_email(email):
        print("Invalid email format.")
        return

    address = input("Enter address (optional): ").strip()
    group = input("Enter group (Friends/Work/Family): ").strip() or "Other"

    contacts[name] = {
        "phone": phone,
        "email": email or None,
        "address": address or None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    print(f"✔ Contact '{name}' added successfully.")


def search_contact(contacts):
    term = input("Enter name to search: ").lower()
    found = False

    for name, info in contacts.items():
        if term in name.lower():
            found = True
            print("\nName:", name)
            print(" Phone:", info["phone"])
            if info["email"]:
                print(" Email:", info["email"])
            if info["address"]:
                print(" Address:", info["address"])
            print(" Group:", info["group"])

    if not found:
        print("No matching contacts found.")


def update_contact(contacts):
    name = input("Enter contact name to update: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    phone = input("Enter new phone (leave blank to keep old): ").strip()
    if phone:
        cleaned = clean_phone(phone)
        if not cleaned:
            print("Invalid phone number.")
            return
        contacts[name]["phone"] = cleaned

    email = input("Enter new email (leave blank to keep old): ").strip()
    if email:
        if not validate_email(email):
            print("Invalid email.")
            return
        contacts[name]["email"] = email

    address = input("Enter new address (leave blank to keep old): ").strip()
    if address:
        contacts[name]["address"] = address

    contacts[name]["updated_at"] = datetime.now().isoformat()
    print(f"✔ Contact '{name}' updated successfully.")


def delete_contact(contacts):
    name = input("Enter contact name to delete: ").strip()

    if name not in contacts:
        print("Contact not found.")
        return

    confirm = input(f"Are you sure you want to delete '{name}'? (y/n): ").lower()
    if confirm == 'y':
        del contacts[name]
        print("✔ Contact deleted.")


def display_all_contacts(contacts):
    if not contacts:
        print("No contacts available.")
        return

    print("\n--- ALL CONTACTS ---")
    for name, info in contacts.items():
        print(f"\n{name}")
        print(" Phone:", info["phone"])
        print(" Group:", info["group"])


# --------------------------------------------------
# Extra Features
# --------------------------------------------------

def export_to_csv(contacts):
    with open("contacts_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone", "Email", "Address", "Group"])

        for name, info in contacts.items():
            writer.writerow([
                name,
                info["phone"],
                info["email"],
                info["address"],
                info["group"]
            ])

    print("✔ Contacts exported to CSV.")


def show_statistics(contacts):
    print("\n--- CONTACT STATISTICS ---")
    print("Total Contacts:", len(contacts))

    groups = {}
    for info in contacts.values():
        grp = info["group"]
        groups[grp] = groups.get(grp, 0) + 1

    for grp, count in groups.items():
        print(f"{grp}: {count} contact(s)")


# --------------------------------------------------
# Menu System
# --------------------------------------------------

def main_menu():
    print("\n" + "=" * 40)
    print("     CONTACT MANAGEMENT SYSTEM")
    print("=" * 40)
    print("1. Add Contact")
    print("2. Search Contact")
    print("3. Update Contact")
    print("4. Delete Contact")
    print("5. View All Contacts")
    print("6. Export to CSV")
    print("7. View Statistics")
    print("8. Exit")


def main():
    contacts = load_contacts()

    while True:
        main_menu()
        choice = input("Enter your choice (1-8): ")

        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            search_contact(contacts)
        elif choice == '3':
            update_contact(contacts)
        elif choice == '4':
            delete_contact(contacts)
        elif choice == '5':
            display_all_contacts(contacts)
        elif choice == '6':
            export_to_csv(contacts)
        elif choice == '7':
            show_statistics(contacts)
        elif choice == '8':
            save_contacts(contacts)
            print("Thank you for using Contact Management System!")
            break
        else:
            print("Invalid choice. Please select 1–8.")


if __name__ == "__main__":
    main()
