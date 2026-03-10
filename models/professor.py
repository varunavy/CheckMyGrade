import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.csv_handler import (
    read_csv, write_csv, append_csv,
    PROFESSOR_FILE, PROFESSOR_HEADERS
)


class Professor:
    def __init__(self, professor_id, professor_name, rank, course_id):
        self.professor_id   = professor_id
        self.professor_name = professor_name
        self.rank           = rank
        self.course_id      = course_id

    def professors_details(self):
        print(f"\n{'='*45}")
        print(f"  Professor ID : {self.professor_id}")
        print(f"  Name         : {self.professor_name}")
        print(f"  Rank         : {self.rank}")
        print(f"  Course ID    : {self.course_id}")
        print(f"{'='*45}")

    @staticmethod
    def add_new_professor(professor_id, professor_name, rank, course_id):
        rows = read_csv(PROFESSOR_FILE, PROFESSOR_HEADERS)
        for row in rows:
            if row["professor_id"] == professor_id:
                print(f"Professor '{professor_id}' already exists.")
                return False
        append_csv(PROFESSOR_FILE, PROFESSOR_HEADERS, {
            "professor_id"  : professor_id,
            "professor_name": professor_name,
            "rank"          : rank,
            "course_id"     : course_id
        })
        print(f"Professor '{professor_id}' added successfully.")
        return True

    @staticmethod
    def delete_professor(professor_id):
        rows = read_csv(PROFESSOR_FILE, PROFESSOR_HEADERS)
        new_rows = [r for r in rows if r["professor_id"] != professor_id]
        if len(new_rows) == len(rows):
            print(f"Professor '{professor_id}' not found.")
            return False
        write_csv(PROFESSOR_FILE, PROFESSOR_HEADERS, new_rows)
        print(f"Professor '{professor_id}' deleted successfully.")
        return True

    @staticmethod
    def modify_professor_details(professor_id, new_name=None, new_rank=None, new_course_id=None):
        rows = read_csv(PROFESSOR_FILE, PROFESSOR_HEADERS)
        found = False
        for row in rows:
            if row["professor_id"] == professor_id:
                if new_name:      row["professor_name"] = new_name
                if new_rank:      row["rank"]           = new_rank
                if new_course_id: row["course_id"]      = new_course_id
                found = True
                break
        if not found:
            print(f"Professor '{professor_id}' not found.")
            return False
        write_csv(PROFESSOR_FILE, PROFESSOR_HEADERS, rows)
        print(f"Professor '{professor_id}' updated successfully.")
        return True

    @staticmethod
    def show_course_details_by_professor(professor_id):
        rows = read_csv(PROFESSOR_FILE, PROFESSOR_HEADERS)
        for row in rows:
            if row["professor_id"] == professor_id:
                print(f"\nProfessor '{row['professor_name']}' teaches Course ID: {row['course_id']}")
                return
        print(f"Professor '{professor_id}' not found.")

    @staticmethod
    def display_all_professors():
        rows = read_csv(PROFESSOR_FILE, PROFESSOR_HEADERS)
        if not rows:
            print("No professors found.")
            return
        for row in rows:
            p = Professor(
                row["professor_id"],
                row["professor_name"],
                row["rank"],
                row["course_id"]
            )
            p.professors_details()


