"""
Password management utility script for DreamHome Real Estate Portal.
Provides functions to reset passwords and update user authentication data.
Run this script when passwords need to be reset or rehashed.
"""
from app import app
from models import db, User
from werkzeug.security import generate_password_hash
import getpass

def get_secure_password(prompt="Enter password: "):
    """
    Securely gets and confirms a password from user input.
    """
    while True:
        password = getpass.getpass(prompt)
        confirm_password = getpass.getpass("Confirm password: ")
        if password != confirm_password:
            print("Passwords do not match. Try again.")
        elif not password:
            print("Password cannot be empty. Try again.")
        else:
            return password

def reset_admin_password():
    """
    Resets the admin password to a known value and updates the hashing method to pbkdf2:sha256.
    """
    with app.app_context():
        admin_users = User.query.filter_by(roleId=1).all()

        if not admin_users:
            print("No admin users found in the database.")
            return

        new_password = get_secure_password("Enter new password for admin user(s): ")
        hashed_password = generate_password_hash(new_password, method='pbkdf2:sha256')

        for admin in admin_users:
            admin.password = hashed_password
            print(f"Updated password for admin: {admin.username}")

        db.session.commit()
        print(f"Successfully updated {len(admin_users)} admin user(s).")

def update_all_user_passwords():
    """
    Updates all user passwords with a temporary password using pbkdf2:sha256 method.
    """
    with app.app_context():
        users = User.query.all()

        if not users:
            print("No users found in the database.")
            return

        temp_password = get_secure_password("Enter temporary password for all users: ")
        hashed_password = generate_password_hash(temp_password, method='pbkdf2:sha256')

        for user in users:
            user.password = hashed_password
            print(f"Updated password for user: {user.username}")

        db.session.commit()
        print(f"Successfully updated {len(users)} user(s).")

if __name__ == "__main__":
    print("Password Hash Fix Utility")
    print("=========================")
    print("1. Reset only admin password")
    print("2. Reset all user passwords")

    choice = input("Enter your choice (1 or 2): ").strip()

    if choice == "1":
        reset_admin_password()
    elif choice == "2":
        update_all_user_passwords()
    else:
        print("Invalid choice. Please run the script again.")
