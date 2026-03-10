import sys
import os
import time
import unittest
import random
import string

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.student    import Student
from models.course     import Course
from models.professor  import Professor
from models.grade      import Grades
from models.login_user import LoginUser
from utils.csv_handler import (
    write_csv,
    STUDENT_FILE,  STUDENT_HEADERS,
    COURSE_FILE,   COURSE_HEADERS,
    PROFESSOR_FILE, PROFESSOR_HEADERS,
    LOGIN_FILE,    LOGIN_HEADERS
)


def reset_all_csv():
    """Wipe all 4 CSV files back to headers only before each test."""
    write_csv(STUDENT_FILE,   STUDENT_HEADERS,   [])
    write_csv(COURSE_FILE,    COURSE_HEADERS,     [])
    write_csv(PROFESSOR_FILE, PROFESSOR_HEADERS,  [])
    write_csv(LOGIN_FILE,     LOGIN_HEADERS,      [])


# ─────────────────────────────────────────────
# 1. STUDENT TESTS
# ─────────────────────────────────────────────
class TestStudent(unittest.TestCase):

    def setUp(self):
        reset_all_csv()

    def test_add_student(self):
        result = Student.add_new_student(
            "sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)
        self.assertTrue(result)
        print("\n[PASS] test_add_student")

    def test_add_duplicate_student(self):
        Student.add_new_student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)
        result = Student.add_new_student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)
        self.assertFalse(result)
        print("[PASS] test_add_duplicate_student")

    def test_delete_student(self):
        Student.add_new_student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)
        result = Student.delete_student("sam@mycsu.edu")
        self.assertTrue(result)
        print("[PASS] test_delete_student")

    def test_delete_nonexistent_student(self):
        result = Student.delete_student("ghost@mycsu.edu")
        self.assertFalse(result)
        print("[PASS] test_delete_nonexistent_student")

    def test_update_student(self):
        Student.add_new_student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)
        result = Student.update_student_record("sam@mycsu.edu", marks=75)
        self.assertTrue(result)
        print("[PASS] test_update_student")

    def test_grade_auto_assigned(self):
        Student.add_new_student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)
        student = Student._load_linked_list().find("sam@mycsu.edu", "email_address")
        self.assertEqual(student.grade, "A")
        print("[PASS] test_grade_auto_assigned")

    def test_1000_students(self):
        """Add 1000 students, verify count, search and sort with timing."""
        print("\n-- Generating 1000 students --")
        start_add = time.time()
        for i in range(1000):
            email = f"student{i}@mycsu.edu"
            fname = f"First{i}"
            lname = f"Last{i}"
            marks = random.uniform(50, 100)
            Student.add_new_student(email, fname, lname, "DATA200", round(marks, 2))
        add_time = time.time() - start_add
        print(f"   Added 1000 students in {add_time:.4f} seconds")

        # Verify count
        ll = Student._load_linked_list()
        self.assertEqual(len(ll), 1000)
        print(f"   Total records in LinkedList: {len(ll)}")

        # Search timing
        start_search = time.time()
        result = Student.search_student("student500@mycsu.edu")
        search_time = time.time() - start_search
        self.assertIsNotNone(result)
        print(f"   Search completed in {search_time:.6f} seconds")

        # Sort by marks timing
        start_sort = time.time()
        Student.sort_by_marks(ascending=True)
        sort_marks_time = time.time() - start_sort
        print(f"   Sort by marks (asc) in {sort_marks_time:.6f} seconds")

        # Sort by email timing
        start_sort2 = time.time()
        Student.sort_by_email(ascending=True)
        sort_email_time = time.time() - start_sort2
        print(f"   Sort by email (asc) in {sort_email_time:.6f} seconds")

        print("[PASS] test_1000_students")


# ─────────────────────────────────────────────
# 2. COURSE TESTS
# ─────────────────────────────────────────────
class TestCourse(unittest.TestCase):

    def setUp(self):
        reset_all_csv()

    def test_add_course(self):
        result = Course.add_new_course("DATA200", "Data Science", "DS and Python", "3")
        self.assertTrue(result)
        print("\n[PASS] test_add_course")

    def test_add_duplicate_course(self):
        Course.add_new_course("DATA200", "Data Science", "DS and Python", "3")
        result = Course.add_new_course("DATA200", "Data Science", "DS and Python", "3")
        self.assertFalse(result)
        print("[PASS] test_add_duplicate_course")

    def test_delete_course(self):
        Course.add_new_course("DATA200", "Data Science", "DS and Python", "3")
        result = Course.delete_new_course("DATA200")
        self.assertTrue(result)
        print("[PASS] test_delete_course")

    def test_modify_course(self):
        Course.add_new_course("DATA200", "Data Science", "DS and Python", "3")
        result = Course.modify_course("DATA200", new_name="Advanced Data Science")
        self.assertTrue(result)
        print("[PASS] test_modify_course")


# ─────────────────────────────────────────────
# 3. PROFESSOR TESTS
# ─────────────────────────────────────────────
class TestProfessor(unittest.TestCase):

    def setUp(self):
        reset_all_csv()

    def test_add_professor(self):
        result = Professor.add_new_professor(
            "michael@mycsu.edu", "Michael John", "Senior Professor", "DATA200")
        self.assertTrue(result)
        print("\n[PASS] test_add_professor")

    def test_add_duplicate_professor(self):
        Professor.add_new_professor(
            "michael@mycsu.edu", "Michael John", "Senior Professor", "DATA200")
        result = Professor.add_new_professor(
            "michael@mycsu.edu", "Michael John", "Senior Professor", "DATA200")
        self.assertFalse(result)
        print("[PASS] test_add_duplicate_professor")

    def test_delete_professor(self):
        Professor.add_new_professor(
            "michael@mycsu.edu", "Michael John", "Senior Professor", "DATA200")
        result = Professor.delete_professor("michael@mycsu.edu")
        self.assertTrue(result)
        print("[PASS] test_delete_professor")

    def test_modify_professor(self):
        Professor.add_new_professor(
            "michael@mycsu.edu", "Michael John", "Senior Professor", "DATA200")
        result = Professor.modify_professor_details(
            "michael@mycsu.edu", new_rank="Lead Professor")
        self.assertTrue(result)
        print("[PASS] test_modify_professor")


# ─────────────────────────────────────────────
# 4. GRADE TESTS
# ─────────────────────────────────────────────
class TestGrades(unittest.TestCase):

    def setUp(self):
        reset_all_csv()
        Student.add_new_student("sam@mycsu.edu", "Sam", "Carpenter", "DATA200", 96)

    def test_get_letter_grade(self):
        self.assertEqual(Grades.get_letter_grade(95), "A")
        self.assertEqual(Grades.get_letter_grade(85), "B")
        self.assertEqual(Grades.get_letter_grade(75), "C")
        self.assertEqual(Grades.get_letter_grade(65), "D")
        self.assertEqual(Grades.get_letter_grade(50), "F")
        print("\n[PASS] test_get_letter_grade")

    def test_modify_grade(self):
        result = Grades.modify_grade("sam@mycsu.edu", "DATA200", 70)
        self.assertTrue(result)
        print("[PASS] test_modify_grade")

    def test_average_score(self):
        Student.add_new_student("alex@mycsu.edu", "Alex", "B", "DATA200", 80)
        avg = Grades.average_score("DATA200")
        self.assertAlmostEqual(avg, 88.0)
        print("[PASS] test_average_score")

    def test_median_score(self):
        Student.add_new_student("alex@mycsu.edu", "Alex", "B", "DATA200", 80)
        median = Grades.median_score("DATA200")
        self.assertAlmostEqual(median, 88.0)
        print("[PASS] test_median_score")


# ─────────────────────────────────────────────
# 5. LOGIN TESTS
# ─────────────────────────────────────────────
class TestLoginUser(unittest.TestCase):

    def setUp(self):
        reset_all_csv()

    def test_register(self):
        result = LoginUser.register("michael@mycsu.edu", "Welcome12#_", "professor")
        self.assertTrue(result)
        print("\n[PASS] test_register")

    def test_login_correct(self):
        LoginUser.register("michael@mycsu.edu", "Welcome12#_", "professor")
        role = LoginUser.login("michael@mycsu.edu", "Welcome12#_")
        self.assertEqual(role, "professor")
        print("[PASS] test_login_correct")

    def test_login_wrong_password(self):
        LoginUser.register("michael@mycsu.edu", "Welcome12#_", "professor")
        role = LoginUser.login("michael@mycsu.edu", "wrongpass")
        self.assertIsNone(role)
        print("[PASS] test_login_wrong_password")

    def test_change_password(self):
        LoginUser.register("michael@mycsu.edu", "Welcome12#_", "professor")
        result = LoginUser.change_password(
            "michael@mycsu.edu", "Welcome12#_", "NewPass99!")
        self.assertTrue(result)
        role = LoginUser.login("michael@mycsu.edu", "NewPass99!")
        self.assertEqual(role, "professor")
        print("[PASS] test_change_password")


if __name__ == "__main__":
    unittest.main(verbosity=2)