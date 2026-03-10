import sys
import os
sys.path.append(os.path.dirname(__file__))

from models.student    import Student
from models.course     import Course
from models.professor  import Professor
from models.grade      import Grades
from models.login_user import LoginUser


current_user = None
current_role = None


def student_menu():
    while True:
        print("\n--- Student Menu ---")
        print("1. Add Student")
        print("2. Delete Student")
        print("3. Update Student")
        print("4. Display All Students")
        print("5. Search Student")
        print("6. Sort by Marks")
        print("7. Sort by Email")
        print("8. Check My Grades")
        print("9. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            email   = input("Email: ").strip()
            fname   = input("First Name: ").strip()
            lname   = input("Last Name: ").strip()
            course  = input("Course ID: ").strip()
            marks   = float(input("Marks: ").strip())
            Student.add_new_student(email, fname, lname, course, marks)
        elif choice == "2":
            email = input("Email to delete: ").strip()
            Student.delete_student(email)
        elif choice == "3":
            email  = input("Email to update: ").strip()
            fname  = input("New First Name (Enter to skip): ").strip() or None
            lname  = input("New Last Name (Enter to skip): ").strip()  or None
            course = input("New Course ID (Enter to skip): ").strip()  or None
            marks  = input("New Marks (Enter to skip): ").strip()
            marks  = float(marks) if marks else None
            Student.update_student_record(email, fname, lname, course, marks)
        elif choice == "4":
            Student.display_all_students()
        elif choice == "5":
            email = input("Email to search: ").strip()
            Student.search_student(email)
        elif choice == "6":
            order = input("Order (asc/desc): ").strip().lower()
            Student.sort_by_marks(ascending=(order == "asc"))
        elif choice == "7":
            order = input("Order (asc/desc): ").strip().lower()
            Student.sort_by_email(ascending=(order == "asc"))
        elif choice == "8":
            email = input("Email: ").strip()
            Student.check_my_grades(email)
        elif choice == "9":
            break
        else:
            print("Invalid choice.")


def course_menu():
    while True:
        print("\n--- Course Menu ---")
        print("1. Add Course")
        print("2. Delete Course")
        print("3. Modify Course")
        print("4. Display All Courses")
        print("5. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            cid   = input("Course ID: ").strip()
            cname = input("Course Name: ").strip()
            desc  = input("Description: ").strip()
            cred  = input("Credits: ").strip()
            Course.add_new_course(cid, cname, desc, cred)
        elif choice == "2":
            cid = input("Course ID to delete: ").strip()
            Course.delete_new_course(cid)
        elif choice == "3":
            cid   = input("Course ID to modify: ").strip()
            cname = input("New Name (Enter to skip): ").strip()       or None
            desc  = input("New Description (Enter to skip): ").strip() or None
            cred  = input("New Credits (Enter to skip): ").strip()    or None
            Course.modify_course(cid, cname, desc, cred)
        elif choice == "4":
            Course.display_all_courses()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def professor_menu():
    while True:
        print("\n--- Professor Menu ---")
        print("1. Add Professor")
        print("2. Delete Professor")
        print("3. Modify Professor")
        print("4. Display All Professors")
        print("5. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            pid   = input("Professor Email/ID: ").strip()
            pname = input("Professor Name: ").strip()
            rank  = input("Rank: ").strip()
            cid   = input("Course ID: ").strip()
            Professor.add_new_professor(pid, pname, rank, cid)
        elif choice == "2":
            pid = input("Professor ID to delete: ").strip()
            Professor.delete_professor(pid)
        elif choice == "3":
            pid   = input("Professor ID to modify: ").strip()
            pname = input("New Name (Enter to skip): ").strip()      or None
            rank  = input("New Rank (Enter to skip): ").strip()      or None
            cid   = input("New Course ID (Enter to skip): ").strip() or None
            Professor.modify_professor_details(pid, pname, rank, cid)
        elif choice == "4":
            Professor.display_all_professors()
        elif choice == "5":
            break
        else:
            print("Invalid choice.")


def grade_menu():
    while True:
        print("\n--- Grade Menu ---")
        print("1. Display Grade Report")
        print("2. Add/Update Grade")
        print("3. Delete Grade")
        print("4. Average Score for Course")
        print("5. Median Score for Course")
        print("6. Back")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            Grades.display_grade_report()
        elif choice == "2":
            email  = input("Student Email: ").strip()
            course = input("Course ID: ").strip()
            marks  = float(input("Marks: ").strip())
            Grades.add_grade(email, course, marks)
        elif choice == "3":
            email  = input("Student Email: ").strip()
            course = input("Course ID: ").strip()
            Grades.delete_grade(email, course)
        elif choice == "4":
            course = input("Course ID: ").strip()
            Grades.average_score(course)
        elif choice == "5":
            course = input("Course ID: ").strip()
            Grades.median_score(course)
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def main_menu():
    while True:
        print("\n===== CheckMyGrade Main Menu =====")
        print("1. Student Records")
        print("2. Course Management")
        print("3. Professor Management")
        print("4. Grade Reports")
        print("5. Logout")
        choice = input("Enter choice: ").strip()

        if   choice == "1": student_menu()
        elif choice == "2": course_menu()
        elif choice == "3": professor_menu()
        elif choice == "4": grade_menu()
        elif choice == "5":
            LoginUser.logout(current_user)
            break
        else:
            print("Invalid choice.")


def main():
    global current_user, current_role
    print("===== Welcome to CheckMyGrade =====")
    while True:
        print("\n1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            email    = input("Email: ").strip()
            password = input("Password: ").strip()
            role = LoginUser.login(email, password)
            if role:
                current_user = email
                current_role = role
                main_menu()
        elif choice == "2":
            email    = input("Email: ").strip()
            password = input("Password: ").strip()
            role     = input("Role (student/professor): ").strip()
            LoginUser.register(email, password, role)
        elif choice == "3":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()