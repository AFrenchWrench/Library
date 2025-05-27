from models.fine import Fine
from models.user import User
from models.book import Book
from models.loan import Loan
from models.author import Author
from models.publisher import Publisher
from models.category import Category
from models.exceptions import (
    ValidationFailedError,
    FineNotFound,
)
from db import get_connection

seeded_author_id = None
seeded_publisher_id = None
seeded_category_id = None
seeded_book_id = None
seeded_user_id = None
seeded_loan_id = None


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def seed_required_foreign_keys():
    global seeded_author_id, seeded_publisher_id, seeded_category_id, seeded_book_id, seeded_user_id, seeded_loan_id

    author = Author(name="FineTest Author")
    author.save()
    seeded_author_id = author.id

    publisher = Publisher(name="FineTest Publisher")
    publisher.save()
    seeded_publisher_id = publisher.id

    category = Category(name="FineTest Category")
    category.save()
    seeded_category_id = category.id

    book = Book(
        isbn="FINE123456",
        title="Fine Test Book",
        author_id=seeded_author_id,
        publisher_id=seeded_publisher_id,
        category_id=seeded_category_id,
        total_copies=2,
        available_copies=2,
    )
    book.save()
    seeded_book_id = book.id

    user = User(name="Fine User", email="fineuser@example.com", password="Test1234$")
    user.save()
    seeded_user_id = user.id

    loan = Loan(user_id=seeded_user_id, book_id=seeded_book_id)
    loan.save()
    seeded_loan_id = loan.id


def delete_seeded_foreign_keys():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM fines WHERE user_id = %s", (seeded_user_id,))
            cur.execute("DELETE FROM loans WHERE id = %s", (seeded_loan_id,))
            cur.execute("DELETE FROM books WHERE id = %s", (seeded_book_id,))
            cur.execute("DELETE FROM users WHERE id = %s", (seeded_user_id,))
            cur.execute("DELETE FROM authors WHERE id = %s", (seeded_author_id,))
            cur.execute("DELETE FROM publishers WHERE id = %s", (seeded_publisher_id,))
            cur.execute("DELETE FROM categories WHERE id = %s", (seeded_category_id,))
            conn.commit()


def test_create_valid_fine():
    try:
        fine = Fine(user_id=seeded_user_id, loan_id=seeded_loan_id, amount=100.0)
        fine.save()
        print_result("Create valid fine", True)
    except Exception as e:
        print_result("Create valid fine", False)
        print(e)
    finally:
        Fine.delete_by_id(fine.id)


def test_invalid_foreign_keys():
    try:
        fine = Fine(user_id=None, loan_id=None, amount=50.0)
        fine.save()
        print_result("Reject fine with null user/loan", False)
    except ValidationFailedError:
        print_result("Reject fine with null user/loan", True)
    except Exception as e:
        print_result("Reject fine with null user/loan", False)
        print(e)


def test_negative_amount():
    try:
        fine = Fine(user_id=seeded_user_id, loan_id=seeded_loan_id, amount=-20.0)
        fine.save()
        print_result("Reject fine with negative amount", False)
    except ValidationFailedError:
        print_result("Reject fine with negative amount", True)
    except Exception as e:
        print_result("Reject fine with negative amount", False)
        print(e)


def test_get_by_id():
    try:
        fine = Fine(user_id=seeded_user_id, loan_id=seeded_loan_id, amount=40.0)
        fine.save()
        fetched = Fine.get_by_id(fine.id)
        if fetched.user_id == seeded_user_id and fetched.loan_id == seeded_loan_id:
            print_result("Get fine by ID", True)
        else:
            print_result("Get fine by ID", False)
    except Exception as e:
        print_result("Get fine by ID", False)
        print(e)
    finally:
        Fine.delete_by_id(fine.id)


def test_get_nonexistent_fine():
    try:
        Fine.get_by_id(-1)
        print_result("Handle non-existent fine", False)
    except FineNotFound:
        print_result("Handle non-existent fine", True)
    except Exception as e:
        print_result("Handle non-existent fine", False)
        print(e)


def test_get_by_user_status_filters():
    try:
        fine1 = Fine(user_id=seeded_user_id, loan_id=seeded_loan_id, amount=10.0)
        fine1.save()

        fine2 = Fine(
            user_id=seeded_user_id, loan_id=seeded_loan_id, amount=20.0, paid=True
        )
        fine2.save()

        all_fines = Fine.get_by_user(seeded_user_id, status="all")
        paid_fines = Fine.get_by_user(seeded_user_id, status="paid")
        unpaid_fines = Fine.get_by_user(seeded_user_id, status="unpaid")

        if len(all_fines) >= 2 and len(paid_fines) >= 1 and len(unpaid_fines) >= 1:
            print_result("Get fine by user and status", True)
        else:
            print_result("Get fine by user and status", False)
    except Exception as e:
        print_result("Get fine by user and status", False)
        print(e)
    finally:
        Fine.delete_by_id(fine1.id)
        Fine.delete_by_id(fine2.id)


def test_get_by_loan():
    try:
        fine = Fine(user_id=seeded_user_id, loan_id=seeded_loan_id, amount=60.0)
        fine.save()
        result = Fine.get_by_loan(seeded_loan_id)
        if result and result.id == fine.id:
            print_result("Get fine by loan", True)
        else:
            print_result("Get fine by loan", False)
    except Exception as e:
        print_result("Get fine by loan", False)
        print(e)
    finally:
        Fine.delete_by_id(fine.id)


def test_delete_fine():
    try:
        fine = Fine(user_id=seeded_user_id, loan_id=seeded_loan_id, amount=35.0)
        fine.save()
        Fine.delete_by_id(fine.id)
        try:
            Fine.get_by_id(fine.id)
            print_result("Delete fine", False)
        except FineNotFound:
            print_result("Delete fine", True)
    except Exception as e:
        print_result("Delete fine", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Fine tests...\n")
    seed_required_foreign_keys()

    try:
        test_create_valid_fine()
        test_invalid_foreign_keys()
        test_negative_amount()
        test_get_by_id()
        test_get_nonexistent_fine()
        test_get_by_user_status_filters()
        test_get_by_loan()
        test_delete_fine()
    finally:
        print("\nCleaning up seeded foreign keys...")
        delete_seeded_foreign_keys()
        print("Cleanup complete.")
