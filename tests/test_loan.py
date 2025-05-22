from datetime import date, timedelta
from models.loan import Loan
from models.db_exceptions import ValidationFailedError
from models.book import Book
from models.member import Member
from models.author import Author
from models.publisher import Publisher
from models.category import Category

seeded_member_id = None
seeded_book_id = None


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def seed_required_foreign_keys():
    global seeded_member_id, seeded_book_id

    Loan.delete_all()
    Book.delete_all()
    Member.delete_all()
    Author.delete_all()
    Publisher.delete_all()
    Category.delete_all()

    member = Member(name="John Doe", email="john@example.com", password="Abcd123#")
    member.save()
    seeded_member_id = member.id

    author = Author(name="Default Author")
    author.save()

    publisher = Publisher(name="Default Publisher")
    publisher.save()

    category = Category(name="Default Category")
    category.save()

    book = Book(
        isbn="9991112223",
        title="Loanable Book",
        author_id=author.id,
        publisher_id=publisher.id,
        category_id=category.id,
        total_copies=3,
        available_copies=3,
    )
    book.save()
    seeded_book_id = book.id


def delete_seeded_foreign_keys():
    Loan.delete_all()
    Book.delete_all()
    Member.delete_all()
    Author.delete_all()
    Publisher.delete_all()
    Category.delete_all()


def test_delete_all_loans():
    try:
        Loan.delete_all()
        print_result("Delete all loans", True)
    except Exception as e:
        print_result("Delete all loans", False)
        print(e)


def test_create_valid_loan():
    try:
        Loan.delete_all()
        loan = Loan(
            member_id=seeded_member_id,
            book_id=seeded_book_id,
            loan_date=date.today(),
            due_date=date.today() + timedelta(days=7),
        )
        loan.save()
        print_result("Create valid loan", True)
    except Exception as e:
        print_result("Create valid loan", False)
        print(e)


def test_invalid_foreign_keys():
    try:
        loan = Loan(
            member_id=9999,
            book_id=9999,
            loan_date=date.today(),
            due_date=date.today() + timedelta(days=7),
        )
        loan.save()
        print_result("Reject invalid foreign keys", False)
    except ValidationFailedError:
        print_result("Reject invalid foreign keys", True)
    except Exception as e:
        print_result("Reject invalid foreign keys", False)
        print(e)


def test_missing_return_date():
    try:
        loan = Loan(
            member_id=seeded_member_id,
            book_id=seeded_book_id,
            loan_date=date.today(),
            due_date=date.today() + timedelta(days=10),
        )
        loan.save()
        print_result("Allow missing return date", True)
    except Exception as e:
        print_result("Allow missing return date", False)
        print(e)


def test_update_return_date():
    try:
        loan = Loan(
            member_id=seeded_member_id,
            book_id=seeded_book_id,
            loan_date=date.today(),
            due_date=date.today() + timedelta(days=5),
        )
        loan.save()

        loan.return_date = date.today() + timedelta(days=3)
        loan.save()

        print_result("Update return date", True)
    except Exception as e:
        print_result("Update return date", False)
        print(e)


def test_invalid_dates():
    try:
        loan = Loan(
            member_id=seeded_member_id,
            book_id=seeded_book_id,
            loan_date="not-a-date",
            due_date="also-not-a-date",
        )
        loan.save()
        print_result("Reject invalid dates", False)
    except ValidationFailedError:
        print_result("Reject invalid dates", True)
    except Exception as e:
        print_result("Reject invalid dates", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Loan tests...\n")
    seed_required_foreign_keys()

    try:
        test_delete_all_loans()
        test_create_valid_loan()
        test_invalid_foreign_keys()
        test_missing_return_date()
        test_update_return_date()
        test_invalid_dates()
    finally:
        print("\nCleaning up seeded foreign keys...")
        delete_seeded_foreign_keys()
        print("Cleanup complete.")
