from db import get_connection
from models.author import Author
from models.book import Book
from models.category import Category
from models.loan import Loan
from models.publisher import Publisher
from models.user import User
from models.exceptions import (
    AdminAlreadyExistsError,
    AuthorInUse,
    BookInUse,
    CategoryInUse,
    PublisherInUse,
    UserInUse,
    UserNotFound,
    ValidationFailedError,
)


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_create_admin():
    try:
        admin = User(
            name="Admin One",
            email="admin@example.com",
            password="Hash123@",
            role="admin",
        )
        admin.save()
        print_result("Create admin", True)
    except Exception as e:
        print_result("Create admin", False)
        print(e)
    finally:
        User.delete_by_email("admin@example.com")


def test_prevent_second_admin():
    try:
        admin = User(
            name="Admin One",
            email="admin@example.com",
            password="Hash123@",
            role="admin",
        )
        admin.save()
        second_admin = User(
            name="Admin Two",
            email="admin2@example.com",
            password="Abc1234#",
            role="admin",
        )
        second_admin.save()
        print_result("Prevent second admin", False)
    except AdminAlreadyExistsError:
        print_result("Prevent second admin", True)
    except Exception as e:
        print_result("Prevent second admin", False)
        print(e)
    finally:
        User.delete_by_email("admin@example.com")


def test_create_user():
    try:
        user = User(
            name="John Doe",
            email="john@example.com",
            password="Abc1234#",
            role="member",
        )
        user.save()
        print_result("Create regular user", True)
    except Exception as e:
        print_result("Create regular user", False)
        print(e)
    finally:
        User.delete_by_email("john@example.com")


def test_invalid_role():
    try:
        bad_user = User(
            name="Hacker",
            email="hack@example.com",
            password="Abc1234#",
            role="superadmin",
        )
        bad_user.save()
        print_result("Invalid role rejected", False)
    except (ValidationFailedError, ValueError):
        print_result("Invalid role rejected", True)
    except Exception as e:
        print_result("Invalid role rejected", False)
        print(e)


def test_get_user_by_id():
    try:
        user = User(
            name="John Doe",
            email="john@example.com",
            password="Abc1234#",
            role="member",
        )
        user.save()
        fetched = User.get_by_id(user.id)
        if fetched.name == "John Doe":
            print_result("Get user by ID", True)
        else:
            print_result("Get user by ID", False)
    except Exception as e:
        print_result("Get user by ID", False)
        print(e)
    finally:
        User.delete_by_email("john@example.com")


def test_get_user_by_email():
    try:
        user = User(
            name="John Doe",
            email="john@example.com",
            password="Abc1234#",
            role="member",
        )
        user.save()
        fetched = User.get_by_email("john@example.com")
        if fetched.name == "John Doe":
            print_result("Get user by email", True)
        else:
            print_result("Get user by email", False)
    except Exception as e:
        print_result("Get user by email", False)
        print(e)
    finally:
        User.delete_by_email("john@example.com")


def test_get_nonexistent_user():
    try:
        User.get_by_email("ghost@example.com")
        print_result("Handle non-existent user", False)
    except UserNotFound:
        print_result("Handle non-existent user", True)
    except Exception as e:
        print_result("Handle non-existent user", False)
        print(e)


def test_update_user():
    try:
        user = User(
            name="John Doe",
            email="john@example.com",
            password="Abc1234#",
            role="member",
        )
        user.save()
        user.name = "Johnny Updated"
        user.save()
        updated = User.get_by_email("john@example.com")
        if updated.name == "Johnny Updated":
            print_result("Update user", True)
        else:
            print_result("Update user", False)
    except Exception as e:
        print_result("Update user", False)
        print(e)
    finally:
        User.delete_by_email("john@example.com")


def test_weak_password_no_uppercase():
    try:
        weak_user = User(
            name="Lowercase Guy",
            email="lower@example.com",
            password="abc1234#",
            role="member",
        )
        weak_user.save()
        print_result("Weak password (no uppercase) rejected", False)
    except ValidationFailedError:
        print_result("Weak password (no uppercase) rejected", True)
    except Exception as e:
        print_result("Weak password (no uppercase) rejected", False)
        print(e)


def test_weak_password_no_special_char():
    try:
        weak_user = User(
            name="NoSpecial",
            email="nospecial@example.com",
            password="Abc12345",
            role="member",
        )
        weak_user.save()
        print_result("Weak password (no special char) rejected", False)
    except ValidationFailedError:
        print_result("Weak password (no special char) rejected", True)
    except Exception as e:
        print_result("Weak password (no special char) rejected", False)
        print(e)


def test_invalid_email_format():
    try:
        bad_email_user = User(
            name="Bad Email",
            email="not-an-email",
            password="Abc1234#",
            role="member",
        )
        bad_email_user.save()
        print_result("Invalid email format rejected", False)
    except ValidationFailedError:
        print_result("Invalid email format rejected", True)
    except Exception as e:
        print_result("Invalid email format rejected", False)
        print(e)


def test_short_name():
    try:
        short_name_user = User(
            name="A",
            email="short@example.com",
            password="Abc1234#",
            role="member",
        )
        short_name_user.save()
        print_result("Too short name rejected", False)
    except ValidationFailedError:
        print_result("Too short name rejected", True)
    except Exception as e:
        print_result("Too short name rejected", False)
        print(e)


def test_missing_fields():
    try:
        incomplete_user = User(
            name="NoEmailNoPass",
            email="",
            password="",
            role="member",
        )
        incomplete_user.save()
        print_result("Missing fields rejected", False)
    except ValidationFailedError:
        print_result("Missing fields rejected", True)
    except Exception as e:
        print_result("Missing fields rejected", False)
        print(e)


def test_delete_user_by_email():
    try:
        user = User(
            name="Temp User",
            email="temp@example.com",
            password="Abc1234#",
            role="member",
        )
        user.save()

        User.delete_by_email("temp@example.com")

        try:
            User.get_by_email("temp@example.com")
            print_result("Delete user by email", False)
        except UserNotFound:
            print_result("Delete user by email", True)
    except Exception as e:
        print_result("Delete user by email", False)
        print(e)


def test_user_in_use():
    try:
        user = User(name="InUse User", email="InUse@gmail.com", password="Abcd1234#")
        user.save()

        author = Author(name="Temp Author")
        author.save()

        publisher = Publisher(name="Temp Publisher")
        publisher.save()

        category = Category(name="Temp Category")
        category.save()

        book = Book(
            isbn="9988776655",
            title="Temp Book",
            author_id=author.id,
            publisher_id=publisher.id,
            category_id=category.id,
            total_copies=5,
            available_copies=5,
        )
        book.save()

        loan = Loan(
            user_id=user.id,
            book_id=book.id,
        )
        loan.save()

        try:
            User.delete_by_email("InUse@gmail.com")
            print_result("Reject deletion of in-use user", False)
        except UserInUse:
            print_result("Reject deletion of in-use user", True)
        except Exception as e:
            print_result("Reject deletion of in-use user", False)
            print(e)

    except Exception as e:
        print_result("Reject deletion of in-use user", False)
        print(e)
    finally:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("DELETE FROM loans WHERE id = %s", (loan.id,))
                conn.commit()
        try:
            User.delete_by_email("InUse@gmail.com")
        except UserInUse:
            pass
        try:
            Book.delete_by_isbn("9988776655")
        except BookInUse:
            pass
        try:
            Publisher.delete_by_name("Temp Publisher")
        except PublisherInUse:
            pass
        try:
            Category.delete_by_name("Temp Category")
        except CategoryInUse:
            pass
        try:
            Author.delete_by_name("Temp Author")
        except AuthorInUse:
            pass


if __name__ == "__main__":
    print("\nRunning User tests...\n")
    test_create_admin()
    test_prevent_second_admin()
    test_create_user()
    test_invalid_role()
    test_get_user_by_id()
    test_get_user_by_email()
    test_get_nonexistent_user()
    test_update_user()
    test_weak_password_no_uppercase()
    test_weak_password_no_special_char()
    test_invalid_email_format()
    test_short_name()
    test_missing_fields()
    test_delete_user_by_email()
    test_user_in_use()
