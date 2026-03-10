import sys
import os
import time
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.csv_handler import (
    read_csv, write_csv, append_csv,
    STUDENT_FILE, STUDENT_HEADERS
)
from utils.linked_list import LinkedList
from models.grade import Grades


class Student:
    def __init__(self, email_address, first_name, last_name, course_id, grade, marks):
        self.email_address = email_address
        self.first_name    = first_name
        self.last_name     = last_name
        self.course_id     = course_id
        self.grade         = grade
        self.marks         = float(marks) if marks else 0.0

    def display_records(self):
        print(f"\n{'='*50}")
        print(f"  Email   : {self.email_address}")
        print(f"  Name    : {self.first_name} {self.last_name}")
        print(f"  Course  : {self.course_id}")
        print(f"  Grade   : {self.grade}")
        print(f"  Marks   : {self.marks}")
        print(f"{'='*50}")

    # ── helpers ──────────────────────────────────────
    @staticmethod
    def _load_linked_list() -> LinkedList:
        """Read students.csv and load every row into a LinkedList."""
        ll = LinkedList()
        for row in read_csv(STUDENT_FILE, STUDENT_HEADERS):
            ll.append(Student(
                row["email_address"], row["first_name"], row["last_name"],
                row["course_id"],     row["grade"],      row["marks"]
            ))
        return ll

    @staticmethod
    def _save_linked_list(ll: LinkedList):
        """Write every Student in the LinkedList back to students.csv."""
        rows = [{
            "email_address": s.email_address,
            "first_name"   : s.first_name,
            "last_name"    : s.last_name,
            "course_id"    : s.course_id,
            "grade"        : s.grade,
            "marks"        : s.marks
        } for s in ll]
        write_csv(STUDENT_FILE, STUDENT_HEADERS, rows)

    # ── CRUD ─────────────────────────────────────────
    @staticmethod
    def add_new_student(email, first_name, last_name, course_id, marks: float):
        ll = Student._load_linked_list()
        # Unique check
        if ll.find(email, "email_address"):
            print(f"Student '{email}' already exists.")
            return False
        grade = Grades.get_letter_grade(marks)
        ll.append(Student(email, first_name, last_name, course_id, grade, marks))
        Student._save_linked_list(ll)
        print(f"Student '{email}' added successfully.")
        return True

    @staticmethod
    def delete_student(email):
        ll = Student._load_linked_list()
        if not ll.delete(email, "email_address"):
            print(f"Student '{email}' not found.")
            return False
        Student._save_linked_list(ll)
        print(f"Student '{email}' deleted successfully.")
        return True

    @staticmethod
    def update_student_record(email, first_name=None, last_name=None,
                               course_id=None, marks=None):
        ll = Student._load_linked_list()
        student = ll.find(email, "email_address")
        if not student:
            print(f"Student '{email}' not found.")
            return False
        if first_name: student.first_name = first_name
        if last_name:  student.last_name  = last_name
        if course_id:  student.course_id  = course_id
        if marks is not None:
            student.marks = float(marks)
            student.grade = Grades.get_letter_grade(float(marks))
        Student._save_linked_list(ll)
        print(f"Student '{email}' updated successfully.")
        return True

    # ── Display ───────────────────────────────────────
    @staticmethod
    def display_all_students():
        ll = Student._load_linked_list()
        if len(ll) == 0:
            print("No students found.")
            return
        for s in ll:
            s.display_records()

    @staticmethod
    def check_my_grades(email):
        ll = Student._load_linked_list()
        student = ll.find(email, "email_address")
        if not student:
            print(f"Student '{email}' not found.")
            return
        print(f"\nGrade for {email}: {student.grade} ({student.marks})")

    # ── Search ────────────────────────────────────────
    @staticmethod
    def search_student(email):
        start = time.time()
        ll = Student._load_linked_list()
        result = ll.find(email, "email_address")
        elapsed = time.time() - start
        print(f"Search completed in {elapsed:.6f} seconds.")
        if result:
            result.display_records()
        else:
            print(f"Student '{email}' not found.")
        return result

    # ── Sort ──────────────────────────────────────────
    @staticmethod
    def sort_by_marks(ascending=True):
        start = time.time()
        ll = Student._load_linked_list()
        students = sorted(ll.to_list(), key=lambda s: s.marks, reverse=not ascending)
        elapsed = time.time() - start
        order = "ascending" if ascending else "descending"
        print(f"\nStudents sorted by marks ({order}) in {elapsed:.6f} seconds:")
        for s in students:
            print(f"  {s.email_address:<30} {s.marks}")
        return students

    @staticmethod
    def sort_by_email(ascending=True):
        start = time.time()
        ll = Student._load_linked_list()
        students = sorted(ll.to_list(), key=lambda s: s.email_address, reverse=not ascending)
        elapsed = time.time() - start
        order = "ascending" if ascending else "descending"
        print(f"\nStudents sorted by email ({order}) in {elapsed:.6f} seconds:")
        for s in students:
            print(f"  {s.email_address:<30} {s.marks}")
        return students


