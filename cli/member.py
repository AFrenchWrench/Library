from datetime import date
from auth import verify_password
from models.author import Author
from models.book import Book
from models.exceptions import (
    BookNotFound,
    DuplicateEmailError,
    FineNotFound,
    LoanNotFound,
    ValidationFailedError,
)
from models.fine import Fine
from models.loan import Loan
from models.publisher import Publisher
from models.user import User

current_user = None


def list_books():
    try:
        print("\n--- Book List ---")
        books = Book.get_all()
        if not books:
            print("There are no books in database")
            return

        for b in books:
            print(
                f"[{b.id}] {b.title}\n Publisher: {Publisher.get_by_id(b.publisher_id).name} Author: {Author.get_by_id(b.author_id).name} (Available: {b.available_copies})"
            )
    except BookNotFound as e:
        print(e)


def view_loans(status="all"):
    try:
        print("\n--- Your Loans ---")
        loans = Loan.get_by_user(current_user.id, status)
        for l in loans:
            print(
                f"Loan ID: {l.id}, Book Title: {Book.get_by_id(l.book_id).title}, Borrowed on: {l.loan_date}, Returned: {l.return_date if l.return_date else "Not returned yet"}"
            )
        return True
    except LoanNotFound as e:
        print(e)
        return False


def list_fines():
    try:
        print("\n--- Your Fines ---")
        fines = Fine.get_by_user(current_user.id)
        for f in fines:
            print(f"Fine ID: {f.id}, Loan ID: {f.loan_id}, Amount: {f.amount}")
    except FineNotFound as e:
        print(e)


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
    if not view_loans("active"):
        return
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


def update_profile():
    print("\n--- Update Profile ---")
    print(f"Current Name: {current_user.name}")
    print(f"Current Email: {current_user.email}")

    name = input("New Name (leave blank to keep current): ").strip()
    email = input("New Email (leave blank to keep current): ").strip()
    password = input("New Password (leave blank to keep current): ").strip()

    if name:
        current_user.name = name
    if email:
        current_user.email = email
    if password:
        while True:
            try:
                old_password = input("Enter your old password: ")
                if verify_password(old_password, current_user.password):
                    current_user.password = password
                    break
                else:
                    print(
                        "Input doesn't match the old password (Press Ctrl+C to cancel)"
                    )
                    continue
            except KeyboardInterrupt:
                break
    try:
        current_user.save()
        print("Profile updated successfully.")
    except ValidationFailedError as e:
        print(e)
    except DuplicateEmailError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def menu(user: User):
    global current_user
    current_user = user
    while True:
        try:
            print(
                """
    ====== Member Menu ======
    1. List Available Books
    2. Borrow Book
    3. View My Loans
    4. Return a Book
    5. View My Fines
    6. Update My Profile
    0. Logout
    ========================="""
            )
            choice = input("Enter your choice: ").strip()

            if choice == "1":
                list_books()
            elif choice == "2":
                borrow_book()
            elif choice == "3":
                view_loans()
            elif choice == "4":
                return_book()
            elif choice == "5":
                list_fines()
            elif choice == "6":
                update_profile()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            continue
