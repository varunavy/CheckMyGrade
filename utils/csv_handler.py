import csv
import os

# Path to the data folder
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")

# File paths
STUDENT_FILE   = os.path.join(DATA_DIR, "students.csv")
COURSE_FILE    = os.path.join(DATA_DIR, "courses.csv")
PROFESSOR_FILE = os.path.join(DATA_DIR, "professors.csv")
LOGIN_FILE     = os.path.join(DATA_DIR, "login.csv")

# Column headers for each file
STUDENT_HEADERS   = ["email_address", "first_name", "last_name", "course_id", "grade", "marks"]
COURSE_HEADERS    = ["course_id", "course_name", "description", "credits"]
PROFESSOR_HEADERS = ["professor_id", "professor_name", "rank", "course_id"]
LOGIN_HEADERS     = ["user_id", "password", "role"]


def _ensure_file(filepath, headers):
    """Create the file with headers if it doesn't exist yet."""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()


def read_csv(filepath, headers):
    """Read all rows from a CSV file and return as a list of dicts."""
    _ensure_file(filepath, headers)
    with open(filepath, "r", newline="") as f:
        reader = csv.DictReader(f)
        return [row for row in reader]


def write_csv(filepath, headers, rows):
    """Overwrite the entire CSV file with new rows."""
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def append_csv(filepath, headers, row):
    """Add a single new row to the end of a CSV file."""
    _ensure_file(filepath, headers)
    with open(filepath, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writerow(row)

