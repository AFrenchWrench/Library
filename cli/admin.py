from time import sleep
from models.author import Author
from models.book import Book
from models.category import Category
from models.exceptions import (
    DuplicateEmailError,
    DuplicateISBNError,
    DuplicateNameError,
    ValidationFailedError,
)
from models.publisher import Publisher
from models.user import User
from models.loan import Loan
from models.fine import Fine


current_user = None


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


def list_books():
    print("\n--- Book List ---")
    books = Book.get_all()
    for b in books:
        sleep(0.15)
        print(
            f"[{b.id}] {b.title}\n Publisher: {Publisher.get_by_id(b.publisher_id).name} Author: {Author.get_by_id(b.author_id).name} (Available: {b.available_copies})"
        )


def list_users():
    print("\n--- User List ---")
    users = User.get_all()
    for u in users:
        sleep(0.15)
        print(f"[{u.id}] {u.name} - {u.email}")


def list_loans():
    print("\n--- Loan List ---")
    loans = Loan.get_all()
    for l in loans:
        sleep(0.15)
        print(
            f"[{l.id}] Book ID: {l.book_id}, User ID: {l.user_id}, Loaned: {l.loan_date}, Due: {l.due_date}, Returned: {l.return_date or 'Not yet'}"
        )


def list_fines():
    print("\n--- Fine List ---")
    fines = Fine.get_all()
    for f in fines:
        sleep(0.15)
        print(
            f"[{f.id}] User ID: {f.user_id}, Loan ID: {f.loan_id}, Amount: {f.amount}, Status: {"Paid" if f.paid else "Not Paid"}"
        )


def update_author():
    print("\n--- Update Author ---")
    try:
        author_id = int(input("Author ID to update: "))
        author = Author.get_by_id(author_id)
        if not author:
            print("Author not found.")
            return
        name = input(f"New Name (current: {author.name}): ").strip() or author.name
        if name:
            author.name = name
        author.save()
        print("Author updated successfully.")
    except ValidationFailedError as e:
        print(e)
    except DuplicateNameError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def update_publisher():
    print("\n--- Update Publisher ---")
    try:
        publisher_id = int(input("Publisher ID to update: "))
        publisher = Publisher.get_by_id(publisher_id)
        if not publisher:
            print("Publisher not found.")
            return
        name = (
            input(f"New Name (current: {publisher.name}): ").strip() or publisher.name
        )
        if name:
            publisher.name = name
        publisher.save()
        print("Publisher updated successfully.")
    except ValidationFailedError as e:
        print(e)
    except DuplicateNameError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def update_category():
    print("\n--- Update Category ---")
    try:
        category_id = int(input("Category ID to update: "))
        category = Category.get_by_id(category_id)
        if not category:
            print("Category not found.")
            return
        name = input(f"New Name (current: {category.name}): ").strip() or category.name
        if name:
            category.name = name
        category.save()
        print("Category updated successfully.")
    except ValidationFailedError as e:
        print(e)
    except DuplicateNameError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def update_user():
    print("\n--- Update User ---")
    try:
        user_id = int(input("User ID to update: "))
        user = User.get_by_id(user_id)
        if not user:
            print("User not found.")
            return
        name = input(f"New Name (current: {user.name}): ").strip() or user.name
        email = input(f"New Email (current: {user.email}): ").strip() or user.email
        if name:
            user.name = name
        if email:
            user.email = email
        user.save()
        print("User updated successfully.")
    except ValidationFailedError as e:
        print(e)
    except DuplicateEmailError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def update_book():
    print("\n--- Update Book ---")
    try:
        book_id = int(input("Book ID to update: "))
        book = Book.get_by_id(book_id)
        if not book:
            print("Book not found.")
            return
        title = input(f"New Title (current: {book.title}): ").strip() or book.title
        isbn = input(f"New ISBN (current: {book.isbn}): ").strip() or book.isbn
        author_id = input(f"New Author ID (current: {book.author_id}): ").strip()
        publisher_id = input(
            f"New Publisher ID (current: {book.publisher_id}): "
        ).strip()
        category_id = input(f"New Category ID (current: {book.category_id}): ").strip()
        total_copies = input(
            f"New Total Copies (current: {book.total_copies}): "
        ).strip()
        if title:
            book.title = title
        if isbn:
            book.isbn = isbn
        if author_id:
            book.author_id = int(author_id) if author_id else book.author_id
        if publisher_id:
            book.publisher_id = int(publisher_id) if publisher_id else book.publisher_id
        if category_id:
            book.category_id = int(category_id) if category_id else book.category_id
        if total_copies:
            book.total_copies = int(total_copies)
            if book.available_copies > book.total_copies:
                book.available_copies = book.total_copies
        book.save()
        print("Book updated successfully.")
    except ValidationFailedError as e:
        print(e)
    except DuplicateISBNError as e:
        print(e)
    except Exception as e:
        print(f"Error: {e}")


def update_fine():
    print("\n--- Update Fine ---")
    try:
        fine_id = int(input("Fine ID to update: "))
        fine = Fine.get_by_id(fine_id)
        if not fine:
            print("Fine not found.")
            return
        paid = input("Is the fine paid ? (Y/N): ")
        fine.paid = True if paid.upper() == "Y" else False
        fine.save()
        print("Fine updated successfully.")
    except Exception as e:
        print(f"Error: {e}")


def menu(user: User):
    global current_user
    current_user = user
    while True:
        try:
            print(
                """
            ====== Admin Menu ======
            1.  Add Book
            2.  Add Author
            3.  Add Publisher
            4.  Add Category
            5.  List Books
            6.  List Users
            7.  List Loans
            8.  List Fines
            9.  Update User
            10. Update Book
            11. Update Author
            12. Update Publisher
            13. Update Category
            14. Update Fine
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
            elif choice == "6":
                list_users()
            elif choice == "7":
                list_loans()
            elif choice == "8":
                list_fines()
            elif choice == "9":
                update_user()
            elif choice == "10":
                update_book()
            elif choice == "11":
                update_author()
            elif choice == "12":
                update_publisher()
            elif choice == "13":
                update_category()
            elif choice == "14":
                update_fine()
            elif choice == "0":
                break
            else:
                print("Invalid choice. Try again.")
        except KeyboardInterrupt:
            continue
