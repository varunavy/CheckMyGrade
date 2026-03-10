import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.csv_handler import (
    read_csv, write_csv, append_csv,
    STUDENT_FILE, STUDENT_HEADERS
)


class Grades:
    # Maps numeric marks to letter grades
    GRADE_SCALE = {
        "A": (90, 100),
        "B": (80, 89),
        "C": (70, 79),
        "D": (60, 69),
        "F": (0,  59)
    }

    def __init__(self, grade_id, grade, marks_range):
        self.grade_id    = grade_id
        self.grade       = grade
        self.marks_range = marks_range

    @staticmethod
    def get_letter_grade(marks: float) -> str:
        """Convert a numeric mark to a letter grade."""
        for letter, (low, high) in Grades.GRADE_SCALE.items():
            if low <= marks <= high:
                return letter
        return "F"

    @staticmethod
    def display_grade_report():
        """Display all student grades from students.csv."""
        rows = read_csv(STUDENT_FILE, STUDENT_HEADERS)
        if not rows:
            print("No grade records found.")
            return
        print(f"\n{'='*55}")
        print(f"  {'Email':<25} {'Course':<10} {'Grade':<6} {'Marks'}")
        print(f"{'='*55}")
        for row in rows:
            print(f"  {row['email_address']:<25} {row['course_id']:<10} "
                  f"{row['grade']:<6} {row['marks']}")
        print(f"{'='*55}")

    @staticmethod
    def add_grade(email, course_id, marks: float):
        """Add or update a grade for a student in a course."""
        rows = read_csv(STUDENT_FILE, STUDENT_HEADERS)
        for row in rows:
            if row["email_address"] == email and row["course_id"] == course_id:
                row["marks"] = str(marks)
                row["grade"] = Grades.get_letter_grade(marks)
                write_csv(STUDENT_FILE, STUDENT_HEADERS, rows)
                print(f"Grade updated for {email} in {course_id}.")
                return True
        print(f"Student '{email}' not found in course '{course_id}'.")
        return False

    @staticmethod
    def delete_grade(email, course_id):
        """Reset a student's grade to empty."""
        rows = read_csv(STUDENT_FILE, STUDENT_HEADERS)
        for row in rows:
            if row["email_address"] == email and row["course_id"] == course_id:
                row["marks"] = ""
                row["grade"] = ""
                write_csv(STUDENT_FILE, STUDENT_HEADERS, rows)
                print(f"Grade deleted for {email} in {course_id}.")
                return True
        print(f"Student '{email}' not found in course '{course_id}'.")
        return False

    @staticmethod
    def modify_grade(email, course_id, new_marks: float):
        """Modify an existing grade — same as add_grade."""
        return Grades.add_grade(email, course_id, new_marks)

    @staticmethod
    def average_score(course_id: str) -> float:
        """Calculate average marks for a course."""
        rows = read_csv(STUDENT_FILE, STUDENT_HEADERS)
        marks = [float(r["marks"]) for r in rows
                 if r["course_id"] == course_id and r["marks"]]
        if not marks:
            print(f"No marks found for course '{course_id}'.")
            return 0.0
        avg = sum(marks) / len(marks)
        print(f"Average score for {course_id}: {avg:.2f}")
        return avg

    @staticmethod
    def median_score(course_id: str) -> float:
        """Calculate median marks for a course."""
        rows = read_csv(STUDENT_FILE, STUDENT_HEADERS)
        marks = sorted([float(r["marks"]) for r in rows
                        if r["course_id"] == course_id and r["marks"]])
        if not marks:
            print(f"No marks found for course '{course_id}'.")
            return 0.0
        n = len(marks)
        mid = n // 2
        median = (marks[mid - 1] + marks[mid]) / 2 if n % 2 == 0 else marks[mid]
        print(f"Median score for {course_id}: {median:.2f}")
        return median


