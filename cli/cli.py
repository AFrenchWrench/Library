import sys
from auth import verify_password
from models.exceptions import UserNotFound, ValidationFailedError
from models.user import User

current_user = None


def login():
    global current_user
    print("\n--- Login ---")
    email = input("Email: ").lower().strip()
    password = input("Password: ").strip()
    try:
        user = User.get_by_email(email)
        if verify_password(password, user.password):
            current_user = user
            print(f"Logged in as: {user.name} ({user.role})")
            return True
        else:
            print("\nWrong Password")
            return False
    except UserNotFound:
        print("\nEmail is wrong")
        return False


def register_user():
    print("\n--- Register User ---")
    name = input("Name: ").strip()
    email = input("Email: ").strip().lower()
    password = input("Password: ").strip()
    role = input("Role (admin/member): ").strip().lower()
    if role not in ("admin", "member"):
        print("Invalid role. Defaulting to 'member'.")
        role = "member"
    user = User(name=name, email=email, password=password, role=role)
    try:
        user.save()
        print(f"User '{name}' registered successfully.")
    except ValidationFailedError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def menu():
    while True:
        try:
            print(
                """
    ======== Library CLI ========
    1. Login
    2. Register
    0. Exit
    ============================="""
            )
            choice = input("Enter your choice: ")

            if choice == "1":
                if login():
                    if current_user.role == "admin":
                        from cli.admin import menu
                    else:
                        from cli.member import menu
                    menu(current_user)
            elif choice == "2":
                register_user()
            elif choice == "0":
                print("Exiting... Bye!")
                sys.exit()
            else:
                print("Invalid choice. Please try again.")
        except KeyboardInterrupt:
            continue


if __name__ == "__main__":
    menu()
