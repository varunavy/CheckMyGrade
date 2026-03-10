import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.csv_handler import (
    read_csv, write_csv, append_csv,
    LOGIN_FILE, LOGIN_HEADERS
)
from utils.encryption import encrypt_password, decrypt_password


class LoginUser:
    def __init__(self, user_id, password, role):
        self.user_id  = user_id
        self.password = password   # always stored encrypted
        self.role     = role

    @staticmethod
    def register(user_id, plain_password, role):
        """Register a new user — password is encrypted before saving."""
        rows = read_csv(LOGIN_FILE, LOGIN_HEADERS)
        for row in rows:
            if row["user_id"] == user_id:
                print(f"User '{user_id}' already exists.")
                return False
        encrypted = encrypt_password(plain_password)
        append_csv(LOGIN_FILE, LOGIN_HEADERS, {
            "user_id" : user_id,
            "password": encrypted,
            "role"    : role
        })
        print(f"User '{user_id}' registered successfully.")
        return True

    @staticmethod
    def login(user_id, plain_password):
        """Login — reads encrypted password, decrypts and compares."""
        rows = read_csv(LOGIN_FILE, LOGIN_HEADERS)
        for row in rows:
            if row["user_id"] == user_id:
                decrypted = decrypt_password(row["password"])
                if decrypted == plain_password:
                    print(f"Login successful! Welcome, {user_id}.")
                    return row["role"]
                else:
                    print("Incorrect password.")
                    return None
        print(f"User '{user_id}' not found.")
        return None

    @staticmethod
    def logout(user_id):
        print(f"User '{user_id}' logged out successfully.")

    @staticmethod
    def change_password(user_id, old_password, new_password):
        """Change password after verifying the old one."""
        rows = read_csv(LOGIN_FILE, LOGIN_HEADERS)
        for row in rows:
            if row["user_id"] == user_id:
                decrypted = decrypt_password(row["password"])
                if decrypted != old_password:
                    print("Old password is incorrect.")
                    return False
                row["password"] = encrypt_password(new_password)
                write_csv(LOGIN_FILE, LOGIN_HEADERS, rows)
                print("Password changed successfully.")
                return True
        print(f"User '{user_id}' not found.")
        return False

    @staticmethod
    def display_all_users():
        rows = read_csv(LOGIN_FILE, LOGIN_HEADERS)
        if not rows:
            print("No users found.")
            return
        print(f"\n{'='*45}")
        for row in rows:
            print(f"  User: {row['user_id']}  | Role: {row['role']}")
        print(f"{'='*45}")


