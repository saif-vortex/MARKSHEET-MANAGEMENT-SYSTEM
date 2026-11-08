
import sqlite3


# 1. Connect to the database
def connect_db():

    connection = sqlite3.connect("marksheet.db")
    connection.execute("PRAGMA foreign_keys = ON")

    return connection


# 2. Create database tables
def create_tables():

    connection = connect_db()
    cursor = connection.cursor()

    # Students table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Students (
        student_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT UNIQUE NOT NULL,
        department TEXT NOT NULL,
        semester INTEGER NOT NULL
    )
    """)

    # Subjects table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Subjects (
        subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject_name TEXT UNIQUE NOT NULL,
        total_marks REAL NOT NULL
    )
    """)

    # Marks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Marks (
        marks_id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER NOT NULL,
        subject_id INTEGER NOT NULL,
        obtained_marks REAL NOT NULL,

        FOREIGN KEY (student_id)
        REFERENCES Students(student_id) ON DELETE CASCADE,

        FOREIGN KEY (subject_id)
        REFERENCES Subjects(subject_id) ON DELETE CASCADE,

        UNIQUE(student_id, subject_id),

        CHECK (obtained_marks >= 0)
    )
    """)

    connection.commit()
    connection.close()

    print("Database tables created successfully!")


# 3. Insert 20 sample students
def insert_sample_students():

    students = [
        ("Ali Ahmed", "TC-001", "Telecommunication", 1),
        ("Sara Khan", "TC-002", "Telecommunication", 1),
        ("Hamza Malik", "TC-003", "Telecommunication", 1),
        ("Ayesha Siddiqui", "TC-004", "Telecommunication", 1),
        ("Usman Raza", "TC-005", "Telecommunication", 1),
        ("Hira Shah", "TC-006", "Telecommunication", 1),
        ("Zain Abbas", "TC-007", "Telecommunication", 1),
        ("Fatima Noor", "TC-008", "Telecommunication", 1),
        ("Ahmed Hassan", "TC-009", "Telecommunication", 1),
        ("Maryam Ali", "TC-010", "Telecommunication", 1),
        ("Bilal Ahmed", "TC-011", "Telecommunication", 1),
        ("Laiba Tariq", "TC-012", "Telecommunication", 1),
        ("Saad Qureshi", "TC-013", "Telecommunication", 1),
        ("Eman Khalid", "TC-014", "Telecommunication", 1),
        ("Daniyal Sheikh", "TC-015", "Telecommunication", 1),
        ("Zoya Imran", "TC-016", "Telecommunication", 1),
        ("Hassan Rauf", "TC-017", "Telecommunication", 1),
        ("Iqra Javed", "TC-018", "Telecommunication", 1),
        ("Abdullah Khan", "TC-019", "Telecommunication", 1),
        ("Mahnoor Fatima", "TC-020", "Telecommunication", 1)
    ]

    connection = connect_db()
    cursor = connection.cursor()

    cursor.executemany("""
    INSERT OR IGNORE INTO Students
    (name, roll_no, department, semester)
    VALUES (?, ?, ?, ?)
    """, students)

    connection.commit()
    connection.close()

    print("Sample student records are ready!")


# 4. Insert seven semester subjects
def insert_default_subjects():

    subjects = [
        ("Calculus and Analytical Geometry (CAG)", 100),
        ("Basic Electrical Engineering (BEE)", 100),
        ("Functional English (FE)", 100),
        ("Islamic Studies (IS)", 100),
        ("Pakistan Studies (PST)", 100),
        ("Essentials of Chemistry (EC)", 100),
        ("IT Fundamentals and Applications (ITFA)", 100)
    ]

    connection = connect_db()
    cursor = connection.cursor()

    cursor.executemany("""
    INSERT OR IGNORE INTO Subjects
    (subject_name, total_marks)
    VALUES (?, ?)
    """, subjects)

    connection.commit()
    connection.close()

    print("Seven semester subjects are ready!")


# 5. Generate demonstration marks for all students
def insert_demo_marks():

    connection = connect_db()
    cursor = connection.cursor()

    cursor.execute("SELECT student_id FROM Students")
    students = cursor.fetchall()

    cursor.execute("SELECT subject_id FROM Subjects")
    subjects = cursor.fetchall()

    for student in students:

        student_id = student[0]

        for subject in subjects:

            subject_id = subject[0]

            # Generate consistent sample marks between 65 and 95
            obtained_marks = 65 + (
                (student_id * 7 + subject_id * 11) % 31
            )

            cursor.execute("""
            INSERT OR IGNORE INTO Marks
            (student_id, subject_id, obtained_marks)
            VALUES (?, ?, ?)
            """, (student_id, subject_id, obtained_marks))

    connection.commit()
    connection.close()

    print("Demonstration marks are ready for all students!")


# 6. Initialize the complete database
def initialize_database():

    create_tables()
    insert_sample_students()
    insert_default_subjects()
    insert_demo_marks()


# Run database setup
if __name__ == "__main__":

    initialize_database()


