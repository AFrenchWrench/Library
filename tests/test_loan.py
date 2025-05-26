from models.loan import Loan
from models.book import Book
from models.user import User
from models.exceptions import (
    ValidationFailedError,
    LoanNotFound,
)
from db import get_connection
from models.author import Author
from models.publisher import Publisher
from models.category import Category

seeded_author_id = None
seeded_publisher_id = None
seeded_category_id = None
seeded_book_id = None
seeded_user_id = None


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def seed_required_foreign_keys():
    global seeded_author_id, seeded_publisher_id, seeded_category_id, seeded_book_id, seeded_user_id

    author = Author(name="LoanTest Author")
    author.save()
    seeded_author_id = author.id

    publisher = Publisher(name="LoanTest Publisher")
    publisher.save()
    seeded_publisher_id = publisher.id

    category = Category(name="LoanTest Category")
    category.save()
    seeded_category_id = category.id

    book = Book(
        isbn="LOAN123456",
        title="Loan Test Book",
        author_id=seeded_author_id,
        publisher_id=seeded_publisher_id,
        category_id=seeded_category_id,
        total_copies=3,
        available_copies=3,
    )
    book.save()
    seeded_book_id = book.id

    user = User(name="Loan User", email="loanuser@example.com", password="Test1234$")
    user.save()
    seeded_user_id = user.id


def delete_seeded_foreign_keys():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM loans WHERE user_id = %s", (seeded_user_id,))
            cur.execute("DELETE FROM books WHERE id = %s", (seeded_book_id,))
            cur.execute("DELETE FROM users WHERE id = %s", (seeded_user_id,))
            cur.execute("DELETE FROM authors WHERE id = %s", (seeded_author_id,))
            cur.execute("DELETE FROM publishers WHERE id = %s", (seeded_publisher_id,))
            cur.execute("DELETE FROM categories WHERE id = %s", (seeded_category_id,))
            conn.commit()


def test_create_valid_loan():
    try:
        loan = Loan(user_id=seeded_user_id, book_id=seeded_book_id)
        loan.save()
        print_result("Create valid loan", True)
    except Exception as e:
        print_result("Create valid loan", False)
        print(e)
    finally:
        Loan.delete_by_id(loan.id)


def test_exceed_active_loans():
    try:
        loan_ids = []
        for i in range(3):
            book = Book(
                isbn=f"LOANEEEEEEX{i}",
                title=f"Loan Limit {i}",
                author_id=seeded_author_id,
                publisher_id=seeded_publisher_id,
                category_id=seeded_category_id,
                total_copies=1,
                available_copies=1,
            )
            book.save()
            loan = Loan(user_id=seeded_user_id, book_id=book.id)
            loan.save()
            loan_ids.append(loan.id)

        extra_book = Book(
            isbn="EXCEEDLIMIT",
            title="Too Many Loans",
            author_id=seeded_author_id,
            publisher_id=seeded_publisher_id,
            category_id=seeded_category_id,
            total_copies=1,
            available_copies=1,
        )
        extra_book.save()

        Loan(user_id=seeded_user_id, book_id=extra_book.id).save()
        print_result("Reject loan beyond active limit", False)
    except ValidationFailedError:
        print_result("Reject loan beyond active limit", True)
    except Exception as e:
        print_result("Reject loan beyond active limit", False)
        print(e)
    finally:
        for i in range(3):
            Loan.delete_by_id(loan_ids[i])
            Book.delete_by_isbn(f"LOANEEEEEEX{i}")
        Book.delete_by_isbn("EXCEEDLIMIT")


def test_book_not_available():
    try:
        book = Book(
            isbn="UNAVAILABLE1",
            title="Unavailable Book",
            author_id=seeded_author_id,
            publisher_id=seeded_publisher_id,
            category_id=seeded_category_id,
            total_copies=0,
            available_copies=0,
        )
        book.save()
        Loan(user_id=seeded_user_id, book_id=book.id).save()
        print_result("Reject loan on unavailable book", False)
    except ValidationFailedError:
        print_result("Reject loan on unavailable book", True)
    except Exception as e:
        print_result("Reject loan on unavailable book", False)
        print(e)
    finally:
        Book.delete_by_isbn("UNAVAILABLE1")


def test_invalid_user_and_book():
    try:
        loan = Loan(user_id=None, book_id=None)
        loan.save()
        print_result("Reject loan with null user/book", False)
    except ValidationFailedError:
        print_result("Reject loan with null user/book", True)
    except Exception as e:
        print_result("Reject loan with null user/book", False)
        print(e)


def test_get_by_id():
    try:
        loan = Loan(user_id=seeded_user_id, book_id=seeded_book_id)
        loan.save()
        fetched = Loan.get_by_id(loan.id)
        if fetched.user_id == seeded_user_id and fetched.book_id == seeded_book_id:
            print_result("Get loan by ID", True)
        else:
            print_result("Get loan by ID", False)
    except Exception as e:
        print_result("Get loan by ID", False)
        print(e)
    finally:
        Loan.delete_by_id(loan.id)


def test_get_nonexistent_loan():
    try:
        Loan.get_by_id(-1)
        print_result("Handle non-existent loan", False)
    except LoanNotFound:
        print_result("Handle non-existent loan", True)
    except Exception as e:
        print_result("Handle non-existent loan", False)
        print(e)


def test_delete_loan():
    try:
        loan = Loan(user_id=seeded_user_id, book_id=seeded_book_id)
        loan.save()
        Loan.delete_by_id(loan.id)
        try:
            Loan.get_by_id(loan.id)
            print_result("Delete loan", False)
        except LoanNotFound:
            print_result("Delete loan", True)
    except Exception as e:
        print_result("Delete loan", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Loan tests...\n")
    seed_required_foreign_keys()

    try:
        test_create_valid_loan()
        test_exceed_active_loans()
        test_book_not_available()
        test_invalid_user_and_book()
        test_get_by_id()
        test_get_nonexistent_loan()
        test_delete_loan()
    finally:
        print("\nCleaning up seeded foreign keys...")
        delete_seeded_foreign_keys()
        print("Cleanup complete.")
