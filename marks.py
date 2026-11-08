
from database import connect_db, initialize_database
from student import get_student_by_id


# 1. Calculate grade and grade points
def calculate_grade(percentage):

    if percentage >= 90:
        return "A+", 4.0

    elif percentage >= 85:
        return "A", 4.0

    elif percentage >= 80:
        return "A-", 3.7

    elif percentage >= 75:
        return "B+", 3.3

    elif percentage >= 70:
        return "B", 3.0

    elif percentage >= 65:
        return "B-", 2.7

    elif percentage >= 60:
        return "C", 2.3

    elif percentage >= 55:
        return "D", 2.0

    else:
        return "F", 0.0


# 2. Retrieve all marks of a student
def get_student_marks(student_id):

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("""
    SELECT
        Subjects.subject_name,
        Subjects.total_marks,
        Marks.obtained_marks

    FROM Marks

    JOIN Subjects
    ON Marks.subject_id = Subjects.subject_id

    WHERE Marks.student_id = ?

    ORDER BY Subjects.subject_id
    """, (student_id,))

    marks = cursor.fetchall()

    connection.close()

    return marks


# 3. Calculate marksheet results
def calculate_results(marks):

    total_obtained = 0
    total_marks = 0

    for mark in marks:

        total_obtained += mark[2]
        total_marks += mark[1]

    if total_marks == 0:
        return 0, 0, "N/A", 0.0

    percentage = (total_obtained / total_marks) * 100

    grade, cgpa = calculate_grade(percentage)

    return (
        total_obtained,
        total_marks,
        grade,
        cgpa
    )


# 4. Display complete student marksheet
def display_student_marksheet(student_id):

    student = get_student_by_id(student_id)

    if student is None:

        print("\nStudent ID does not exist!")
        return

    marks = get_student_marks(student_id)

    if len(marks) == 0:

        print("\nNo marks found for this student!")
        return

    # Student information
    print("\n")
    print("=" * 55)
    print("             STUDENT MARKSHEET")
    print("=" * 55)

    print("Student ID:", student[0])
    print("Student Name:", student[1])
    print("Roll Number:", student[2])
    print("Department:", student[3])
    print("Semester:", student[4])

    print("-" * 55)

    # Subject-wise marks
    print("\nSUBJECT-WISE RESULTS\n")

    print("{:<35} {:>8} {:>8} {:>6}".format(
        "Subject", "Obtained", "Total", "Grade"
    ))

    print("-" * 62)

    for mark in marks:

        subject_name = mark[0]
        total_marks = mark[1]
        obtained_marks = mark[2]

        subject_percentage = (
            obtained_marks / total_marks
        ) * 100

        subject_grade, subject_cgpa = calculate_grade(
            subject_percentage
        )

        print("{:<35} {:>8.1f} {:>8.1f} {:>6}".format(
            subject_name,
            obtained_marks,
            total_marks,
            subject_grade
        ))

    print("-" * 62)

    # Overall calculations
    total_obtained, total_marks, grade, cgpa = (
        calculate_results(marks)
    )

    percentage = (total_obtained / total_marks) * 100

    print("\nOVERALL RESULT")
    print("-" * 35)

    print("Total Obtained Marks:", total_obtained)
    print("Total Maximum Marks:", total_marks)

    print("Percentage:", round(percentage, 2), "%")
    print("Overall Grade:", grade)
    print("CGPA:", cgpa, "/ 4.0")

    print("=" * 55)


# 5. Main program
if __name__ == "__main__":

    # Prepare database and sample records
    initialize_database()

    print("\n======================================")
    print("       STUDENT MARKSHEET SYSTEM")
    print("======================================")

    try:

        student_id = int(input("\nEnter Student ID: "))

        display_student_marksheet(student_id)

    except ValueError:

        print("Invalid input! Please enter a numeric Student ID.")



