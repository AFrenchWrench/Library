from models.category import Category
from models.db_exceptions import ValidationFailedError


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_delete_all():
    try:
        Category.delete_all()
        print_result("Delete all categories", True)
    except Exception as e:
        print_result("Delete all categories", False)
        print(e)


def test_create_category():
    try:
        Category.delete_all()
        category = Category(name="Fiction")
        category.save()
        print_result("Create category", True)
    except Exception as e:
        print_result("Create category", False)
        print(e)


def test_empty_name():
    try:
        category = Category(name="")
        category.save()
        print_result("Reject empty category name", False)
    except ValidationFailedError:
        print_result("Reject empty category name", True)
    except Exception as e:
        print_result("Reject empty category name", False)
        print(e)


if __name__ == "__main__":
    print("Running Category tests...\n")
    test_delete_all()
    test_create_category()
    test_empty_name()
