from models.member import Member
from models.db_exceptions import AdminAlreadyExistsError, UserNotFound
from auth import hash_password


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_delete_all():
    try:
        Member.delete_all_members()
        print_result("Delete all members", True)
    except Exception as e:
        print_result("Delete all members", False)
        print(e)


def test_create_admin():
    try:
        Member.delete_all_members()
        admin = Member(
            name="Admin One",
            email="admin@example.com",
            password_hash=hash_password("hash123"),
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
            password_hash=hash_password("hash456"),
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
            password_hash=hash_password("abc123"),
            role="member",
        )
        user.save()
        print_result("Create regular user", True)
    except Exception as e:
        print_result("Create regular user", False)
        print(e)


def test_invalid_role():
    try:
        Member(
            name="Hacker",
            email="hack@example.com",
            password_hash=hash_password("bad"),
            role="superadmin",
        )
        print_result("Invalid role rejected", False)
    except ValueError:
        print_result("Invalid role rejected", True)


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


if __name__ == "__main__":
    print("Running tests...\n")
    test_delete_all()
    test_create_admin()
    test_prevent_second_admin()
    test_create_user()
    test_invalid_role()
    test_get_user_by_email()
    test_get_nonexistent_user()
    test_update_user()
