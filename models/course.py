import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.csv_handler import (
    read_csv, write_csv, append_csv,
    COURSE_FILE, COURSE_HEADERS
)


class Course:
    def __init__(self, course_id, course_name, description, credits):
        self.course_id   = course_id
        self.course_name = course_name
        self.description = description
        self.credits     = credits

    def display_courses(self):
        print(f"\n{'='*45}")
        print(f"  Course ID   : {self.course_id}")
        print(f"  Name        : {self.course_name}")
        print(f"  Description : {self.description}")
        print(f"  Credits     : {self.credits}")
        print(f"{'='*45}")

    @staticmethod
    def add_new_course(course_id, course_name, description, credits):
        rows = read_csv(COURSE_FILE, COURSE_HEADERS)
        for row in rows:
            if row["course_id"] == course_id:
                print(f"Course '{course_id}' already exists.")
                return False
        append_csv(COURSE_FILE, COURSE_HEADERS, {
            "course_id"  : course_id,
            "course_name": course_name,
            "description": description,
            "credits"    : credits
        })
        print(f"Course '{course_id}' added successfully.")
        return True

    @staticmethod
    def delete_new_course(course_id):
        rows = read_csv(COURSE_FILE, COURSE_HEADERS)
        new_rows = [r for r in rows if r["course_id"] != course_id]
        if len(new_rows) == len(rows):
            print(f"Course '{course_id}' not found.")
            return False
        write_csv(COURSE_FILE, COURSE_HEADERS, new_rows)
        print(f"Course '{course_id}' deleted successfully.")
        return True

    @staticmethod
    def modify_course(course_id, new_name=None, new_description=None, new_credits=None):
        rows = read_csv(COURSE_FILE, COURSE_HEADERS)
        found = False
        for row in rows:
            if row["course_id"] == course_id:
                if new_name:        row["course_name"] = new_name
                if new_description: row["description"] = new_description
                if new_credits:     row["credits"]     = new_credits
                found = True
                break
        if not found:
            print(f"Course '{course_id}' not found.")
            return False
        write_csv(COURSE_FILE, COURSE_HEADERS, rows)
        print(f"Course '{course_id}' updated successfully.")
        return True

    @staticmethod
    def display_all_courses():
        rows = read_csv(COURSE_FILE, COURSE_HEADERS)
        if not rows:
            print("No courses found.")
            return
        for row in rows:
            c = Course(
                row["course_id"],
                row["course_name"],
                row["description"],
                row["credits"]
            )
            c.display_courses()

