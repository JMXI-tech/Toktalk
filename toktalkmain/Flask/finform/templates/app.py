import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DB_NAME = "school.db"

# 1. Database Setup
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            grade REAL
        )
    """)

    conn.commit()
    conn.close()


# 2. Add Student
def add_student():
    name = entry_name.get().strip()
    age = entry_age.get().strip()
    grade = entry_grade.get().strip()

    if not name:
        messagebox.showwarning("Input Error", "Name is required")
        return

    try:
        age = int(age) if age else None
        grade = float(grade) if grade else None
    except ValueError:
        messagebox.showwarning(
            "Input Error",
            "Age must be a whole number and Grade must be a number."
        )
        return

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "INSERT INTO students (name, age, grade) VALUES (?, ?, ?)",
        (name, age, grade)
    )

    conn.commit()
    conn.close()

    clear_entries()
    load_students()

    messagebox.showinfo("Success", "Student Added Successfully")


# 3. Load/Display Students
def load_students():
    for row in tree.get_children():
        tree.delete(row)

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("SELECT * FROM students")
    rows = c.fetchall()

    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)


# 4. Delete Student
def delete_student():
    selected = tree.focus()

    if not selected:
        messagebox.showwarning(
            "Selection Error",
            "Please select a student to delete."
        )
        return

    student_id = tree.item(selected)["values"][0]

    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()
    conn.close()

    load_students()

    messagebox.showinfo("Success", "Student Deleted Successfully")


# 5. Clear Input Fields
def clear_entries():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_grade.delete(0, tk.END)


# 6. Build GUI
root = tk.Tk()
root.title("Student Database - Tkinter + SQLite")
root.geometry("500x400")


# Input Frame
frame_input = tk.Frame(root)
frame_input.pack(pady=10)


tk.Label(frame_input, text="Name:").grid(
    row=0, column=0, padx=5, pady=5
)

entry_name = tk.Entry(frame_input)
entry_name.grid(
    row=0, column=1, padx=5, pady=5
)


tk.Label(frame_input, text="Age:").grid(
    row=1, column=0, padx=5, pady=5
)

entry_age = tk.Entry(frame_input)
entry_age.grid(
    row=1, column=1, padx=5, pady=5
)


tk.Label(frame_input, text="Grade:").grid(
    row=2, column=0, padx=5, pady=5
)

entry_grade = tk.Entry(frame_input)
entry_grade.grid(
    row=2, column=1, padx=5, pady=5
)


tk.Button(
    frame_input,
    text="Add Student",
    command=add_student
).grid(
    row=3,
    column=0,
    columnspan=2,
    pady=5
)


tk.Button(
    frame_input,
    text="Delete Selected",
    command=delete_student
).grid(
    row=4,
    column=0,
    columnspan=2
)


# Table Frame
frame_table = tk.Frame(root)
frame_table.pack(
    pady=10,
    fill="both",
    expand=True
)


# Table Columns
columns = ("id", "name", "age", "grade")

tree = ttk.Treeview(
    frame_table,
    columns=columns,
    show="headings"
)

tree.heading("id", text="ID")
tree.heading("name", text="Name")
tree.heading("age", text="Age")
tree.heading("grade", text="Grade")

tree.pack(
    fill="both",
    expand=True
)


# 7. Run Application
init_db()
load_students()

root.mainloop()