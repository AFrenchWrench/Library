from datetime import date, timedelta
from models.fine import Fine
from models.loan import Loan
from models.book import Book
from models.member import Member
from models.author import Author
from models.publisher import Publisher
from models.category import Category
from models.db_exceptions import ValidationFailedError

seeded_member_id = None
seeded_loan_id = None
seeded_book_id = None


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def seed_required_foreign_keys():
    global seeded_member_id, seeded_loan_id, seeded_book_id

    Fine.delete_all()
    Loan.delete_all()
    Book.delete_all()
    Member.delete_all()
    Author.delete_all()
    Publisher.delete_all()
    Category.delete_all()

    member = Member(
        name="Fine Test User", email="fineuser@example.com", password="Fine#123"
    )
    member.save()
    seeded_member_id = member.id

    author = Author(name="Fine Author")
    author.save()

    publisher = Publisher(name="Fine Publisher")
    publisher.save()

    category = Category(name="Fine Category")
    category.save()

    book = Book(
        isbn="FINETEST1234",
        title="Fining Book",
        author_id=author.id,
        publisher_id=publisher.id,
        category_id=category.id,
        total_copies=1,
        available_copies=1,
    )
    book.save()
    seeded_book_id = book.id

    loan = Loan(
        member_id=seeded_member_id,
        book_id=seeded_book_id,
        loan_date=date.today() + timedelta(days=5),
        due_date=date.today() + timedelta(days=10),
    )
    loan.save()
    seeded_loan_id = loan.id


def delete_seeded_foreign_keys():
    Fine.delete_all()
    Loan.delete_all()
    Book.delete_all()
    Member.delete_all()
    Author.delete_all()
    Publisher.delete_all()
    Category.delete_all()


def test_create_valid_fine():
    try:
        fine = Fine(
            member_id=seeded_member_id,
            loan_id=seeded_loan_id,
            amount=5000,
            paid=False,
        )
        fine.save()
        print_result("Create valid fine", True)
    except Exception as e:
        print_result("Create valid fine", False)
        print(e)


def test_invalid_foreign_keys():
    try:
        fine = Fine(
            member_id=9999,
            loan_id=9999,
            amount=5000,
            paid=False,
        )
        fine.save()
        print_result("Reject invalid foreign keys", False)
    except ValidationFailedError:
        print_result("Reject invalid foreign keys", True)
    except Exception as e:
        print_result("Reject invalid foreign keys", False)
        print(e)


def test_non_boolean_paid():
    try:
        fine = Fine(
            member_id=seeded_member_id,
            loan_id=seeded_loan_id,
            amount=1000,
            paid="yes",
        )
        fine.save()
        print_result("Reject non-boolean 'paid'", False)
    except ValidationFailedError:
        print_result("Reject non-boolean 'paid'", True)
    except Exception as e:
        print_result("Reject non-boolean 'paid'", False)
        print(e)


def test_invalid_amount():
    try:
        fine = Fine(
            member_id=seeded_member_id,
            loan_id=seeded_loan_id,
            amount=12.75,
            paid=False,
        )
        fine.save()
        print_result("Reject non-integer amount", False)
    except ValidationFailedError:
        print_result("Reject non-integer amount", True)
    except Exception as e:
        print_result("Reject non-integer amount", False)
        print(e)


def test_update_fine():
    try:
        fine = Fine(
            member_id=seeded_member_id,
            loan_id=seeded_loan_id,
            amount=8000,
            paid=False,
        )
        fine.save()

        fine.amount = 9000
        fine.paid = True
        fine.save()

        print_result("Update fine amount and status", True)
    except Exception as e:
        print_result("Update fine amount and status", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Fine tests...\n")
    seed_required_foreign_keys()

    try:
        test_create_valid_fine()
        test_invalid_foreign_keys()
        test_non_boolean_paid()
        test_invalid_amount()
        test_update_fine()
    finally:
        print("\nCleaning up seeded foreign keys...")
        delete_seeded_foreign_keys()
        print("Cleanup complete.")
