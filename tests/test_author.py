from models.author import Author
from models.db_exceptions import ValidationFailedError, DatabaseOperationError


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_delete_all():
    try:
        Author.delete_all()
        print_result("Delete all authors", True)
    except Exception as e:
        print_result("Delete all authors", False)
        print(e)


def test_create_author():
    try:
        Author.delete_all()
        author = Author(name="John Steinbeck")
        author.save()
        print_result("Create author", True)
    except Exception as e:
        print_result("Create author", False)
        print(e)


def test_short_name():
    try:
        author = Author(name="Jo")
        author.save()
        print_result("Reject short author name", False)
    except ValidationFailedError:
        print_result("Reject short author name", True)
    except Exception as e:
        print_result("Reject short author name", False)
        print(e)


def test_long_name():
    try:
        author = Author(name="A" * 30)
        author.save()
        print_result("Reject long author name", False)
    except ValidationFailedError:
        print_result("Reject long author name", True)
    except Exception as e:
        print_result("Reject long author name", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Author tests...\n")
    test_delete_all()
    test_create_author()
    test_short_name()
    test_long_name()
