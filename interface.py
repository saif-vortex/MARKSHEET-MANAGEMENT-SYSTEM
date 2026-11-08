
import tkinter as tk
from tkinter import ttk, messagebox
import database
import student
import marks


def start_app():

    # ---------------- MAIN WINDOW ----------------

    r = tk.Tk()
    r.title("MARKSHEET MANAGEMENT SYSTEM")
    r.geometry("1200x700")
    r.minsize(950, 650)
    r.configure(bg="#F1F5F9")

    sidebar_color = "#172554"
    bg_color = "#F1F5F9"
    card_color = "white"
    text_color = "#1E293B"
    accent_color = "#2563EB"

    # ---------------- MAIN LAYOUT ----------------

    sidebar = tk.Frame(r, bg=sidebar_color, width=250)
    sidebar.pack(side="left", fill="y")
    sidebar.pack_propagate(False)

    content = tk.Frame(r, bg=bg_color)
    content.pack(side="right", fill="both", expand=True)

    # ---------------- SIDEBAR TITLE ----------------

    tk.Label(
        sidebar,
        text="STUDENT\nMARKSHEET",
        font=("Arial", 20, "bold"),
        bg=sidebar_color,
        fg="white",
        justify="left"
    ).pack(pady=35, padx=20, anchor="w")

    tk.Label(
        sidebar,
        text="MANAGEMENT SYSTEM",
        font=("Arial", 9, "bold"),
        bg=sidebar_color,
        fg="#93C5FD"
    ).pack(anchor="w", padx=20, pady=(0, 25))

    # ---------------- PAGE CONTAINER ----------------

    page_frame = tk.Frame(content, bg=bg_color)
    page_frame.pack(fill="both", expand=True, padx=25, pady=25)

    def clear_page():
        for widget in page_frame.winfo_children():
            widget.destroy()

    def page_title(title, subtitle="Manage your student records"):
        tk.Label(
            page_frame,
            text=title,
            font=("Arial", 23, "bold"),
            bg=bg_color,
            fg=text_color
        ).pack(anchor="w", pady=(0, 5))

        tk.Label(
            page_frame,
            text=subtitle,
            font=("Arial", 10),
            bg=bg_color,
            fg="#64748B"
        ).pack(anchor="w", pady=(0, 25))

    def create_card(parent, title, value, color):
        card = tk.Frame(
            parent,
            bg=card_color,
            padx=20,
            pady=22,
            highlightbackground=color,
            highlightthickness=1
        )

        card.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10
        )

        tk.Label(
            card,
            text=title,
            bg=card_color,
            fg="#64748B",
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            card,
            text=value,
            bg=card_color,
            fg=color,
            font=("Arial", 25, "bold")
        ).pack(anchor="w", pady=(10, 0))

    def create_form(parent):
        form = tk.Frame(
            parent,
            bg=card_color,
            padx=25,
            pady=25
        )
        form.pack(fill="x", pady=10)
        return form

    def create_label(parent, text):
        tk.Label(
            parent,
            text=text,
            font=("Arial", 11, "bold"),
            bg=card_color,
            fg=text_color
        ).pack(anchor="w", pady=(10, 5))

    def create_entry(parent):
        entry = tk.Entry(
            parent,
            font=("Arial", 11),
            relief="solid",
            bd=1
        )
        entry.pack(fill="x", ipady=7)
        return entry

    def create_button(parent, text, command, color=accent_color):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg="white",
            font=("Arial", 10, "bold"),
            relief="flat",
            cursor="hand2",
            padx=18,
            pady=9
        )

    def create_table(parent, columns, headings):
        table_frame = tk.Frame(parent, bg=card_color)
        table_frame.pack(fill="both", expand=True, pady=10)

        tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for column, heading in zip(columns, headings):
            tree.heading(column, text=heading)
            tree.column(column, width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=tree.yview
        )

        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return tree

    # ---------------- DASHBOARD ----------------

    def show_dashboard():
        clear_page()
        page_title(
            "Dashboard",
            "Welcome to Student Marksheet Management System"
        )

        conn = database.connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM Students")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Subjects")
        total_subjects = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Marks")
        total_marks = cursor.fetchone()[0]

        conn.close()

        cards = tk.Frame(page_frame, bg=bg_color)
        cards.pack(fill="x", pady=20)

        create_card(
            cards, "Total Students",
            str(total_students), "#2563EB"
        )

        create_card(
            cards, "Total Subjects",
            str(total_subjects), "#16A34A"
        )

        create_card(
            cards, "Marks Records",
            str(total_marks), "#9333EA"
        )

        welcome = tk.Frame(
            page_frame,
            bg=card_color,
            padx=25,
            pady=25
        )
        welcome.pack(fill="x", pady=25)

        tk.Label(
            welcome,
            text="Welcome!",
            font=("Arial", 18, "bold"),
            bg=card_color,
            fg=text_color
        ).pack(anchor="w")

        tk.Label(
            welcome,
            text=(
                "Use the sidebar to manage students, "
                "subjects, marks and marksheets."
            ),
            font=("Arial", 11),
            bg=card_color,
            fg="#64748B"
        ).pack(anchor="w", pady=10)

    # ---------------- ADD STUDENT ----------------

    def show_add_student():
        clear_page()
        page_title("Add Student", "Register a new student")

        form = create_form(page_frame)

        create_label(form, "Student Name")
        name_entry = create_entry(form)

        create_label(form, "Roll Number")
        roll_entry = create_entry(form)

        create_label(form, "Department")
        department_entry = create_entry(form)
        department_entry.insert(0, "Telecommunication")

        create_label(form, "Semester")
        semester_entry = create_entry(form)

        def save_student():
            name = name_entry.get().strip()
            roll = roll_entry.get().strip()
            department = department_entry.get().strip()
            semester = semester_entry.get().strip()

            if not name or not roll or not department or not semester:
                messagebox.showerror(
                    "Error", "Please fill all fields."
                )
                return

            try:
                semester_number = int(semester)

                if semester_number < 1:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Error", "Enter a valid semester number."
                )
                return

            conn = database.connect_db()

            try:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    INSERT INTO Students
                    (name, roll_no, department, semester)
                    VALUES (?, ?, ?, ?)
                    """,
                    (name, roll, department, semester_number)
                )

                conn.commit()

                messagebox.showinfo(
                    "Success", "Student added successfully!"
                )

                show_add_student()

            except Exception as e:
                messagebox.showerror("Error", str(e))

            finally:
                conn.close()

        create_button(
            form, "Save Student", save_student
        ).pack(anchor="w", pady=20)

    # ---------------- VIEW STUDENTS ----------------

    def show_view_students():
        clear_page()
        page_title("View Students", "All registered students")

        tree = create_table(
            page_frame,
            ("id", "name", "roll", "department", "semester"),
            ("ID", "Name", "Roll Number", "Department", "Semester")
        )

        for record in student.get_all_students():
            tree.insert("", "end", values=record)

    # ---------------- SEARCH STUDENT ----------------

    def show_search_student():
        clear_page()
        page_title("Search Student", "Find a student using roll number")

        form = create_form(page_frame)

        create_label(form, "Enter Roll Number")
        roll_entry = create_entry(form)

        result_frame = tk.Frame(page_frame, bg=bg_color)
        result_frame.pack(fill="x", pady=15)

        def search():
            for widget in result_frame.winfo_children():
                widget.destroy()

            roll = roll_entry.get().strip()

            if not roll:
                messagebox.showerror(
                    "Error", "Enter a roll number."
                )
                return

            conn = database.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM Students WHERE roll_no = ?",
                (roll,)
            )

            record = cursor.fetchone()
            conn.close()

            if record:
                tk.Label(
                    result_frame,
                    text="Student Found",
                    font=("Arial", 15, "bold"),
                    bg=bg_color,
                    fg="#16A34A"
                ).pack(anchor="w", pady=10)

                details = (
                    ("Student ID", record[0]),
                    ("Name", record[1]),
                    ("Roll Number", record[2]),
                    ("Department", record[3]),
                    ("Semester", record[4])
                )

                for label, value in details:
                    tk.Label(
                        result_frame,
                        text=f"{label}: {value}",
                        font=("Arial", 12),
                        bg=bg_color,
                        fg=text_color
                    ).pack(anchor="w", pady=4)

            else:
                messagebox.showinfo(
                    "Not Found", "No student found with this roll number."
                )

        create_button(
            form, "Search Student", search
        ).pack(anchor="w", pady=20)

    # ---------------- UPDATE STUDENT ----------------

    def show_update_student():
        clear_page()
        page_title("Update Student", "Update existing student information")

        form = create_form(page_frame)

        create_label(form, "Roll Number of Student")
        roll_entry = create_entry(form)

        create_label(form, "New Student Name")
        name_entry = create_entry(form)

        create_label(form, "New Department")
        department_entry = create_entry(form)

        create_label(form, "New Semester")
        semester_entry = create_entry(form)

        def update():
            roll = roll_entry.get().strip()
            name = name_entry.get().strip()
            department = department_entry.get().strip()
            semester = semester_entry.get().strip()

            if not roll or not name or not department or not semester:
                messagebox.showerror(
                    "Error", "Please fill all fields."
                )
                return

            try:
                semester_number = int(semester)

                if semester_number < 1:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Error", "Enter a valid semester."
                )
                return

            conn = database.connect_db()

            try:
                cursor = conn.cursor()

                cursor.execute(
                    """
                    UPDATE Students
                    SET name = ?, department = ?, semester = ?
                    WHERE roll_no = ?
                    """,
                    (name, department, semester_number, roll)
                )

                conn.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo(
                        "Success", "Student updated successfully!"
                    )
                    show_update_student()
                else:
                    messagebox.showinfo(
                        "Not Found", "Student does not exist."
                    )

            except Exception as e:
                messagebox.showerror("Error", str(e))

            finally:
                conn.close()

        create_button(
            form, "Update Student", update
        ).pack(anchor="w", pady=20)

    # ---------------- DELETE STUDENT ----------------

    def show_delete_student():
        clear_page()
        page_title("Delete Student", "Remove a student record")

        form = create_form(page_frame)

        create_label(form, "Enter Student Roll Number")
        roll_entry = create_entry(form)

        def delete():
            roll = roll_entry.get().strip()

            if not roll:
                messagebox.showerror(
                    "Error", "Enter a roll number."
                )
                return

            confirm = messagebox.askyesno(
                "Confirm Delete",
                f"Are you sure you want to delete {roll}?"
            )

            if not confirm:
                return

            conn = database.connect_db()

            try:
                cursor = conn.cursor()

                cursor.execute(
                    "DELETE FROM Students WHERE roll_no = ?",
                    (roll,)
                )

                conn.commit()

                if cursor.rowcount > 0:
                    messagebox.showinfo(
                        "Success", "Student deleted successfully!"
                    )
                    show_delete_student()
                else:
                    messagebox.showinfo(
                        "Not Found", "Student does not exist."
                    )

            except Exception as e:
                messagebox.showerror("Error", str(e))

            finally:
                conn.close()

        create_button(
            form, "Delete Student", delete, "#DC2626"
        ).pack(anchor="w", pady=20)

    # ---------------- MANAGE MARKS ----------------

    def show_manage_marks():
        clear_page()
        page_title("Manage Marks", "Add or update student marks")

        form = create_form(page_frame)

        create_label(form, "Student Roll Number")
        roll_entry = create_entry(form)

        create_label(form, "Select Subject")

        conn = database.connect_db()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT subject_id, subject_name, total_marks FROM Subjects"
        )

        subjects = cursor.fetchall()
        conn.close()

        subject_values = [
            f"{s[0]} - {s[1]} (Total: {s[2]})"
            for s in subjects
        ]

        subject_combo = ttk.Combobox(
            form,
            values=subject_values,
            state="readonly",
            font=("Arial", 11)
        )
        subject_combo.pack(fill="x", ipady=5)

        create_label(form, "Obtained Marks")
        obtained_entry = create_entry(form)

        def save_marks():
            roll = roll_entry.get().strip()
            selected = subject_combo.get()
            obtained = obtained_entry.get().strip()

            if not roll or not selected or not obtained:
                messagebox.showerror(
                    "Error", "Please fill all fields."
                )
                return

            try:
                subject_id = int(selected.split(" - ")[0])
                obtained_marks = float(obtained)

            except ValueError:
                messagebox.showerror(
                    "Error", "Enter valid marks."
                )
                return

            conn = database.connect_db()

            try:
                cursor = conn.cursor()

                cursor.execute(
                    "SELECT student_id FROM Students WHERE roll_no = ?",
                    (roll,)
                )
                student_record = cursor.fetchone()

                if not student_record:
                    messagebox.showerror(
                        "Error", "Student not found."
                    )
                    return

                cursor.execute(
                    "SELECT total_marks FROM Subjects WHERE subject_id = ?",
                    (subject_id,)
                )
                subject_record = cursor.fetchone()

                if not subject_record:
                    messagebox.showerror(
                        "Error", "Subject not found."
                    )
                    return

                total_marks = subject_record[0]

                if obtained_marks < 0 or obtained_marks > total_marks:
                    messagebox.showerror(
                        "Error",
                        f"Marks must be between 0 and {total_marks}."
                    )
                    return

                student_id = student_record[0]

                cursor.execute(
                    """
                    SELECT marks_id FROM Marks
                    WHERE student_id = ? AND subject_id = ?
                    """,
                    (student_id, subject_id)
                )

                existing = cursor.fetchone()

                if existing:
                    cursor.execute(
                        """
                        UPDATE Marks
                        SET obtained_marks = ?
                        WHERE student_id = ? AND subject_id = ?
                        """,
                        (obtained_marks, student_id, subject_id)
                    )
                else:
                    cursor.execute(
                        """
                        INSERT INTO Marks
                        (student_id, subject_id, obtained_marks)
                        VALUES (?, ?, ?)
                        """,
                        (student_id, subject_id, obtained_marks)
                    )

                conn.commit()

                messagebox.showinfo(
                    "Success", "Marks saved successfully!"
                )

                obtained_entry.delete(0, tk.END)

            except Exception as e:
                messagebox.showerror("Error", str(e))

            finally:
                conn.close()

        create_button(
            form, "Save Marks", save_marks
        ).pack(anchor="w", pady=20)

    # ---------------- GENERATE MARKSHEET ----------------

    def show_marksheet():
        clear_page()
        page_title("Generate Marksheet", "View a student's complete result")

        form = create_form(page_frame)

        create_label(form, "Enter Student Roll Number")
        roll_entry = create_entry(form)

        result_frame = tk.Frame(page_frame, bg=bg_color)
        result_frame.pack(fill="both", expand=True)

        def generate():
            for widget in result_frame.winfo_children():
                widget.destroy()

            roll = roll_entry.get().strip()

            if not roll:
                messagebox.showerror(
                    "Error", "Enter a roll number."
                )
                return

            conn = database.connect_db()
            cursor = conn.cursor()

            cursor.execute(
                "SELECT * FROM Students WHERE roll_no = ?",
                (roll,)
            )

            record = cursor.fetchone()
            conn.close()

            if not record:
                messagebox.showerror(
                    "Not Found", "Student does not exist."
                )
                return

            student_id = record[0]
            student_marks = marks.get_student_marks(student_id)

            if not student_marks:
                messagebox.showinfo(
                    "No Marks", "No marks have been entered for this student."
                )
                return

            tk.Label(
                result_frame,
                text=f"Name: {record[1]}",
                font=("Arial", 12, "bold"),
                bg=bg_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

            tk.Label(
                result_frame,
                text=f"Roll Number: {record[2]}",
                font=("Arial", 11),
                bg=bg_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

            tk.Label(
                result_frame,
                text=f"Department: {record[3]}",
                font=("Arial", 11),
                bg=bg_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

            tree = create_table(
                result_frame,
                ("subject", "obtained", "total", "grade"),
                ("Subject", "Obtained Marks", "Total Marks", "Grade")
            )

            for subject_name, total, obtained in student_marks:
                percentage = (
                    (obtained / total) * 100 if total else 0
                )

                grade, cgpa = marks.calculate_grade(percentage)

                tree.insert(
                    "",
                    "end",
                    values=(
                        subject_name,
                        obtained,
                        total,
                        grade
                    )
                )

            total_obtained, total_marks, overall_grade, cgpa = (
                marks.calculate_results(student_marks)
            )

            percentage = (
                (total_obtained / total_marks) * 100
                if total_marks else 0
            )

            summary = tk.Frame(
                result_frame,
                bg=card_color,
                padx=20,
                pady=15
            )
            summary.pack(fill="x", pady=10)

            tk.Label(
                summary,
                text=f"Total Obtained: {total_obtained} / {total_marks}",
                font=("Arial", 12, "bold"),
                bg=card_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary,
                text=f"Percentage: {percentage:.2f}%",
                font=("Arial", 12, "bold"),
                bg=card_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary,
                text=f"Overall Grade: {overall_grade}",
                font=("Arial", 12, "bold"),
                bg=card_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

            tk.Label(
                summary,
                text=f"CGPA: {cgpa}",
                font=("Arial", 12, "bold"),
                bg=card_color,
                fg=text_color
            ).pack(anchor="w", pady=3)

        create_button(
            form, "Generate Marksheet", generate
        ).pack(anchor="w", pady=20)

    # ---------------- SIDEBAR NAVIGATION ----------------

    def create_nav_button(text, command):
        button = tk.Button(
            sidebar,
            text=text,
            command=command,
            font=("Arial", 11),
            bg=sidebar_color,
            fg="white",
            activebackground="#1E40AF",
            activeforeground="white",
            relief="flat",
            anchor="w",
            padx=25,
            pady=12,
            cursor="hand2"
        )

        button.pack(fill="x", padx=8, pady=2)

        return button

    create_nav_button("Dashboard", show_dashboard)
    create_nav_button("Add Student", show_add_student)
    create_nav_button("View Students", show_view_students)
    create_nav_button("Search Student", show_search_student)
    create_nav_button("Update Student", show_update_student)
    create_nav_button("Delete Student", show_delete_student)
    create_nav_button("Manage Marks", show_manage_marks)
    create_nav_button("Generate Marksheet", show_marksheet)

    # ---------------- START APPLICATION ----------------

    show_dashboard()
    r.mainloop()
