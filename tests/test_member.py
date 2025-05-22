from models.member import Member
from models.db_exceptions import (
    AdminAlreadyExistsError,
    UserNotFound,
    ValidationFailedError,
)


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_delete_all():
    try:
        Member.delete_all()
        print_result("Delete all members", True)
    except Exception as e:
        print_result("Delete all members", False)
        print(e)


def test_create_admin():
    try:
        Member.delete_all()
        admin = Member(
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


def test_prevent_second_admin():
    try:
        second_admin = Member(
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


def test_create_user():
    try:
        user = Member(
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


def test_invalid_role():
    try:
        bad_user = Member(
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


def test_get_user_by_email():
    try:
        user = Member.get_by_email("john@example.com")
        print_result("Get user by email", True)
    except Exception as e:
        print_result("Get user by email", False)
        print(e)


def test_get_nonexistent_user():
    try:
        Member.get_by_email("ghost@example.com")
        print_result("Handle non-existent user", False)
    except UserNotFound:
        print_result("Handle non-existent user", True)
    except Exception as e:
        print_result("Handle non-existent user", False)
        print(e)


def test_update_user():
    try:
        user = Member.get_by_email("john@example.com")
        user.name = "Johnny Updated"
        user.save()
        updated = Member.get_by_email("john@example.com")
        if updated.name == "Johnny Updated":
            print_result("Update user", True)
        else:
            print_result("Update user", False)
    except Exception as e:
        print_result("Update user", False)
        print(e)


def test_weak_password_no_uppercase():
    try:
        weak_user = Member(
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
        weak_user = Member(
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
        bad_email_user = Member(
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
        short_name_user = Member(
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
        incomplete_user = Member(
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
        user = Member(
            name="Temp User",
            email="temp@example.com",
            password="Abc1234#",
            role="member",
        )
        user.save()

        Member.delete_by_email("temp@example.com")

        try:
            Member.get_by_email("temp@example.com")
            print_result("Delete user by email", False)
        except UserNotFound:
            print_result("Delete user by email", True)
    except Exception as e:
        print_result("Delete user by email", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Member tests...\n")
    test_delete_all()
    test_create_admin()
    test_prevent_second_admin()
    test_create_user()
    test_invalid_role()
    test_get_user_by_email()
    test_get_nonexistent_user()
    test_update_user()
    test_weak_password_no_uppercase()
    test_weak_password_no_special_char()
    test_invalid_email_format()
    test_short_name()
    test_missing_fields()
    test_delete_user_by_email()
