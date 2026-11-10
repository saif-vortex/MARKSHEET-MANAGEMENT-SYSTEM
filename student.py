
import sqlite3
from database import connect_db


# 1. Add a new student
def add_student(name, roll_no, department, semester):

    connection = connect_db()
    cursor = connection.cursor()

    try:

        cursor.execute("""
        INSERT INTO Students
        (name, roll_no, department, semester)
        VALUES (?, ?, ?, ?)
        """, (name, roll_no, department, semester))

        connection.commit()

        print("Student registered successfully!")

    except sqlite3.IntegrityError:

        print("Error: Roll number already exists!")

    finally:
        connection.close()


# 2. Retrieve all students
def get_all_students():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM Students
    ORDER BY student_id
    """)

    students = cursor.fetchall()

    connection.close()

    return students


# 3. Display all students
def display_students():

    students = get_all_students()

    print("\n========== REGISTERED STUDENTS ==========")

    if len(students) == 0:

        print("No student records found!")

    else:

        for student in students:

            print("\nStudent ID:", student[0])
            print("Name:", student[1])
            print("Roll Number:", student[2])
            print("Department:", student[3])
            print("Semester:", student[4])
            print("----------------------------------------")


# 4. Search student by ID
def get_student_by_id(student_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM Students
    WHERE student_id = ?
    """, (student_id,))

    student = cursor.fetchone()

    connection.close()

    return student


# 5. Search student by roll number
def search_student(roll_no):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT * FROM Students
    WHERE roll_no = ?
    """, (roll_no,))

    student = cursor.fetchone()

    connection.close()

    if student:
        print("\nStudent Found!")
        print("Student ID:", student[0])
        print("Name:", student[1])
        print("Roll Number:", student[2])
        print("Department:", student[3])
        print("Semester:", student[4])

    else:
        print("Student not found!")


# 6. Update student information
def update_student(roll_no, name, department, semester):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    UPDATE Students
    SET name = ?, department = ?, semester = ?
    WHERE roll_no = ?
    """, (name, department, semester, roll_no))

    connection.commit()

    if cursor.rowcount > 0:
        print("Student information updated successfully!")

    else:
        print("Student not found!")

    connection.close()


# 7. Delete student record
def delete_student(roll_no):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    DELETE FROM Students
    WHERE roll_no = ?
    """, (roll_no,))

    connection.commit()

    if cursor.rowcount > 0:
        print("Student deleted successfully!")

    else:
        print("Student not found!")

    connection.close()


# Testing section
if __name__ == "__main__":

    display_students()
