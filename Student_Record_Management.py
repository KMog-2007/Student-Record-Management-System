import csv
import json
import os

CSV_FILE = "students.csv"
JSON_FILE = "Students.json"


def initialize_files():
    """Create CSV and JSON files if they do not exist."""

    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="") as file:
            writer = csv.DictWriter(
                file,
                fieldnames=["student_id", "name", "department", "year", "email", "marks"]
            )
            writer.writeheader()

    if not os.path.exists(JSON_FILE):
        with open(JSON_FILE, "w") as file:
            json.dump([], file, indent=4)


def load_students():
    """Load student records from CSV file."""

    try:
        with open(CSV_FILE, "r", newline="") as file:
            return list(csv.DictReader(file))
    except FileNotFoundError:
        return []


def save_students(students):
    """Save student records to CSV and JSON files."""

    fieldnames = ["student_id", "name", "department", "year", "email", "marks"]

    with open(CSV_FILE, "w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(students)

    with open(JSON_FILE, "w") as file:
        json.dump(students, file, indent=4)


def add_student():
    """Add a new student record."""

    students = load_students()

    try:
        student_id = input("Enter Student ID: ").strip()

        if any(student["student_id"] == student_id for student in students):
            print("Student ID already exists.")
            return

        name = input("Enter Name: ").strip()
        department = input("Enter Department: ").strip()
        year = input("Enter Year: ").strip()
        email = input("Enter Email: ").strip()

        marks = float(input("Enter Marks: "))

        if marks < 0 or marks > 100:
            raise ValueError("Marks must be between 0 and 100.")

        student = {
            "student_id": student_id,
            "name": name,
            "department": department,
            "year": year,
            "email": email,
            "marks": marks
        }

        students.append(student)
        save_students(students)

        print("Student added successfully.")

    except ValueError as error:
        print("Invalid input:", error)
    except Exception as error:
        print("An error occurred:", error)
    finally:
        print("Add operation completed.")


def view_students():
    """Display all student records."""

    students = load_students()

    if not students:
        print("No student records found.")
        return

    print("\n" + "=" * 85)
    print(f"{'ID':<10}{'Name':<20}{'Department':<15}{'Year':<8}{'Email':<25}{'Marks':<8}")
    print("=" * 85)

    for student in students:
        print(
            f"{student['student_id']:<10}"
            f"{student['name']:<20}"
            f"{student['department']:<15}"
            f"{student['year']:<8}"
            f"{student['email']:<25}"
            f"{student['marks']:<8}"
        )

    print("=" * 85)


def search_student():
    """Search for a student using Student ID."""

    students = load_students()

    student_id = input("Enter Student ID to search: ").strip()

    result = [
        student for student in students
        if student["student_id"] == student_id
    ]

    if result:
        student = result[0]

        print("\nStudent Found")
        print("-------------------------")
        print("Student ID :", student["student_id"])
        print("Name       :", student["name"])
        print("Department :", student["department"])
        print("Year       :", student["year"])
        print("Email      :", student["email"])
        print("Marks      :", student["marks"])
    else:
        print("Student not found.")


def update_student():
    """Update an existing student record."""

    students = load_students()

    student_id = input("Enter Student ID to update: ").strip()

    for student in students:
        if student["student_id"] == student_id:

            print("\nLeave a field empty to keep the existing value.")

            name = input(f"Name [{student['name']}]: ").strip()
            department = input(
                f"Department [{student['department']}]: "
            ).strip()
            year = input(f"Year [{student['year']}]: ").strip()
            email = input(f"Email [{student['email']}]: ").strip()
            marks = input(f"Marks [{student['marks']}]: ").strip()

            if name:
                student["name"] = name

            if department:
                student["department"] = department

            if year:
                student["year"] = year

            if email:
                student["email"] = email

            if marks:
                try:
                    new_marks = float(marks)

                    if new_marks < 0 or new_marks > 100:
                        raise ValueError("Marks must be between 0 and 100.")

                    student["marks"] = new_marks

                except ValueError as error:
                    print("Invalid marks:", error)
                    return

            save_students(students)

            print("Student record updated successfully.")
            return

    print("Student not found.")


def delete_student():
    """Delete a student record."""

    students = load_students()

    student_id = input("Enter Student ID to delete: ").strip()

    new_students = [
        student for student in students
        if student["student_id"] != student_id
    ]

    if len(new_students) == len(students):
        print("Student not found.")
        return

    save_students(new_students)

    print("Student record deleted successfully.")


def sort_students():
    """Display students sorted by marks."""

    students = load_students()

    if not students:
        print("No student records found.")
        return

    sorted_students = sorted(
        students,
        key=lambda student: float(student["marks"]),
        reverse=True
    )

    print("\nStudents Sorted by Marks")
    print("=" * 50)

    for student in sorted_students:
        print(
            f"{student['student_id']} - "
            f"{student['name']} - "
            f"{student['marks']}"
        )


def main():
    """Main menu of the application."""

    initialize_files()

    while True:

        print("\n")
        print("=" * 45)
        print("   STUDENT RECORD MANAGEMENT SYSTEM")
        print("=" * 45)
        print("1. Add Student")
        print("2. View Students")
        print("3. Search Student")
        print("4. Update Student")
        print("5. Delete Student")
        print("6. Sort Students by Marks")
        print("7. Exit")
        print("=" * 45)

        try:
            choice = int(input("Enter your choice: "))

            if choice == 1:
                add_student()

            elif choice == 2:
                view_students()

            elif choice == 3:
                search_student()

            elif choice == 4:
                update_student()

            elif choice == 5:
                delete_student()

            elif choice == 6:
                sort_students()

            elif choice == 7:
                print("Thank you for using the Student Record Management System.")
                break

            else:
                print("Please enter a number between 1 and 7.")

        except ValueError:
            print("Invalid input. Please enter a number.")

        except Exception as error:
            print("Unexpected error:", error)


if __name__ == "__main__":
    main()
