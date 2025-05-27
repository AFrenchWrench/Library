from datetime import date
import sys
from auth import verify_password
from models.author import Author
from models.category import Category
from models.exceptions import LoanNotFound, UserNotFound, ValidationFailedError
from models.publisher import Publisher
from models.user import User
from models.book import Book
from models.loan import Loan

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


def add_book():
    print("\n--- Add Book ---")
    title = input("Title: ").strip()
    isbn = input("ISBN: ").strip()
    author_id = int(input("Author ID: "))
    publisher_id = int(input("Publisher ID: "))
    category_id = int(input("Category ID: "))
    total_copies = int(input("Total Copies: "))
    book = Book(
        title=title,
        isbn=isbn,
        author_id=author_id,
        publisher_id=publisher_id,
        category_id=category_id,
        total_copies=total_copies,
        available_copies=total_copies,
    )
    try:
        book.save()
        print(f"Book '{title}' added successfully.")
    except ValidationFailedError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def add_author():
    print("\n--- Add Author ---")
    name = input("Author Name: ").strip()
    author = Author(name=name)
    try:
        author.save()
        print(f"Author '{name}' added successfully.")
    except ValidationFailedError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def add_publisher():
    print("\n--- Add Publisher ---")
    name = input("Publisher Name: ").strip()
    publisher = Publisher(name=name)
    try:
        publisher.save()
        print(f"Publisher '{name}' added successfully.")
    except ValidationFailedError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def add_category():
    print("\n--- Add Category ---")
    name = input("Category Name: ").strip()
    category = Category(name=name)
    try:
        category.save()
        print(f"Category '{name}' added successfully.")
    except ValidationFailedError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def borrow_book():
    print("\n--- Borrow Book ---")
    book_id = int(input("Book ID: "))
    try:
        loan = Loan(user_id=current_user.id, book_id=book_id)
        loan.save()
        print("Book borrowed successfully.")
    except ValidationFailedError as e:
        if "active loans" in e:
            print("You already borrowed 3 books that you have not returned")
            return
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def return_book():
    print("\n--- Return Book ---")
    loan_id = int(input("Loan ID: "))
    try:
        loan = Loan.get_by_id(loan_id=loan_id)
        loan.return_date = date.today()
        loan.save()

        fine = loan.check_for_fine()
        if fine:
            print(f"A fine was issued for the delay in return amount: {fine.amount}")
        print("Book returned successfully.")
    except LoanNotFound as e:
        print(e)
    except ValidationFailedError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def list_books():
    print("\n--- Book List ---")
    books = Book.get_all()
    for b in books:
        print(
            f"[{b.id}] {b.title}\n Publisher: {Publisher.get_by_id(b.publisher_id).name} Author: {Author.get_by_id(b.author_id).name} (Available: {b.available_copies})"
        )


def view_loans():
    print("\n--- Your Loans ---")
    loans = Loan.get_by_user(current_user.id)
    for l in loans:
        print(
            f"Loan ID: {l.id}, Book Title: {Book.get_by_id(l.book_id).title}, Borrowed on: {l.loan_date}, Returned: {l.return_date if l.return_date else "Not returned yet"}"
        )


def admin_menu():
    while True:
        try:
            print(
                """
            ====== Admin Menu ======
            1. Add Book
            2. Add Author
            3. Add Publisher
            4. Add Category
            5. List Books
            0. Logout
            ========================"""
            )
            choice = input("Enter your choice: ")

            if choice == "1":
                add_book()
            elif choice == "2":
                add_author()
            elif choice == "3":
                add_publisher()
            elif choice == "4":
                add_category()
            elif choice == "5":
                list_books()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            continue


def member_menu():
    while True:
        try:
            print(
                """
    ====== Member Menu ======
    1. List Available Books
    2. Borrow Book
    3. View My Loans
    0. Logout
    ========================="""
            )
            choice = input("Enter your choice: ")

            if choice == "1":
                list_books()
            elif choice == "2":
                borrow_book()
            elif choice == "3":
                view_loans()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")

        except KeyboardInterrupt:
            continue


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
                        admin_menu()
                    else:
                        member_menu()
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
