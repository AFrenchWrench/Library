from models.book import Book
from models.db_exceptions import (
    ValidationFailedError,
    DuplicateISBNError,
    DatabaseOperationError,
    BookNotFound,
)
from db import get_connection


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def seed_required_foreign_keys():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT IGNORE INTO authors (id, name) VALUES (1, 'Default Author')"
            )
            cur.execute(
                "INSERT IGNORE INTO publishers (id, name) VALUES (1, 'Default Publisher')"
            )
            cur.execute(
                "INSERT IGNORE INTO categories (id, name) VALUES (1, 'Default Category')"
            )
            conn.commit()


def delete_seeded_foreign_keys():
    Book.delete_all()
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM authors WHERE id = 1 AND name = 'Default Author'")
            cur.execute(
                "DELETE FROM publishers WHERE id = 1 AND name = 'Default Publisher'"
            )
            cur.execute(
                "DELETE FROM categories WHERE id = 1 AND name = 'Default Category'"
            )
            conn.commit()


def test_delete_all():
    try:
        Book.delete_all()
        print_result("Delete all books", True)
    except Exception as e:
        print_result("Delete all books", False)
        print(e)


def test_create_valid_book():
    try:
        Book.delete_all()
        book = Book(
            isbn="1234567890",
            title="Python in Depth",
            author_id=1,
            publisher_id=1,
            category_id=1,
            total_copies=5,
            available_copies=5,
        )
        book.save()
        print_result("Create valid book", True)
    except Exception as e:
        print_result("Create valid book", False)
        print(e)


def test_duplicate_isbn():
    try:
        duplicate = Book(
            isbn="1234567890",
            title="Duplicate Book",
            author_id=1,
            publisher_id=1,
            category_id=1,
            total_copies=2,
            available_copies=2,
        )
        duplicate.save()
        print_result("Reject duplicate ISBN", False)
    except DuplicateISBNError:
        print_result("Reject duplicate ISBN", True)
    except Exception as e:
        print_result("Reject duplicate ISBN", False)
        print(e)


def test_short_isbn():
    try:
        book = Book(
            isbn="123",
            title="Short ISBN",
            author_id=1,
            publisher_id=1,
            category_id=1,
        )
        book.save()
        print_result("Reject short ISBN", False)
    except ValidationFailedError:
        print_result("Reject short ISBN", True)
    except Exception as e:
        print_result("Reject short ISBN", False)
        print(e)


def test_long_isbn():
    try:
        book = Book(
            isbn="X" * 25,
            title="Long ISBN",
            author_id=1,
            publisher_id=1,
            category_id=1,
        )
        book.save()
        print_result("Reject long ISBN", False)
    except ValidationFailedError:
        print_result("Reject long ISBN", True)
    except Exception as e:
        print_result("Reject long ISBN", False)
        print(e)


def test_invalid_title():
    try:
        book = Book(
            isbn="1234567899",
            title="پایتون",  # Non-English
            author_id=1,
            publisher_id=1,
            category_id=1,
        )
        book.save()
        print_result("Reject non-English title", False)
    except ValidationFailedError:
        print_result("Reject non-English title", True)
    except Exception as e:
        print_result("Reject non-English title", False)
        print(e)


def test_empty_fields():
    try:
        book = Book(
            isbn="",
            title="",
            author_id=None,
            publisher_id=None,
            category_id=None,
        )
        book.save()
        print_result("Reject empty fields", False)
    except ValidationFailedError:
        print_result("Reject empty fields", True)
    except Exception as e:
        print_result("Reject empty fields", False)
        print(e)


def test_get_by_isbn():
    try:
        book = Book.get_by_isbn("1234567890")
        if book.title == "Python in Depth":
            print_result("Get book by ISBN", True)
        else:
            print_result("Get book by ISBN", False)
    except Exception as e:
        print_result("Get book by ISBN", False)
        print(e)


def test_get_nonexistent_book():
    try:
        Book.get_by_isbn("0000000000")
        print_result("Handle non-existent book", False)
    except BookNotFound:
        print_result("Handle non-existent book", True)
    except Exception as e:
        print_result("Handle non-existent book", False)
        print(e)


def test_update_book_title():
    try:
        book = Book.get_by_isbn("1234567890")
        book.title = "Updated Python Book"
        book.save()
        updated = Book.get_by_isbn("1234567890")
        if updated.title == "Updated Python Book":
            print_result("Update book title", True)
        else:
            print_result("Update book title", False)
    except Exception as e:
        print_result("Update book title", False)
        print(e)


def test_total_less_than_available():
    try:
        book = Book(
            isbn="9876543210",
            title="Logical Test",
            author_id=1,
            publisher_id=1,
            category_id=1,
            total_copies=2,
            available_copies=5,
        )
        book.save()
        print_result("Reject available > total", False)
    except ValidationFailedError:
        print_result("Reject available > total", True)
    except Exception as e:
        print_result("Reject available > total", False)
        print(e)


def test_negative_copies():
    try:
        book = Book(
            isbn="1112223334",
            title="Negative Copies",
            author_id=1,
            publisher_id=1,
            category_id=1,
            total_copies=-1,
            available_copies=-2,
        )
        book.save()
        print_result("Reject negative copy counts", False)
    except ValidationFailedError:
        print_result("Reject negative copy counts", True)
    except Exception as e:
        print_result("Reject negative copy counts", False)
        print(e)


# ------------- Entry Point -------------

if __name__ == "__main__":
    print("\nRunning Book tests...\n")
    seed_required_foreign_keys()

    try:
        test_delete_all()
        test_create_valid_book()
        test_duplicate_isbn()
        test_short_isbn()
        test_long_isbn()
        test_invalid_title()
        test_empty_fields()
        test_get_by_isbn()
        test_get_nonexistent_book()
        test_update_book_title()
        test_total_less_than_available()
        test_negative_copies()
    finally:
        print("\nCleaning up seeded foreign keys...")
        delete_seeded_foreign_keys()
        print("Cleanup complete.")
