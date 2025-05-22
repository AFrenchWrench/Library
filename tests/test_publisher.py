from models.publisher import Publisher
from models.exceptions import ValidationFailedError


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_delete_all():
    try:
        Publisher.delete_all()
        print_result("Delete all publishers", True)
    except Exception as e:
        print_result("Delete all publishers", False)
        print(e)


def test_create_publisher():
    try:
        Publisher.delete_all()
        publisher = Publisher(name="Penguin Books")
        publisher.save()
        print_result("Create publisher", True)
    except Exception as e:
        print_result("Create publisher", False)
        print(e)


def test_invalid_name():
    try:
        publisher = Publisher(name="پنگوئن")
        publisher.save()
        print_result("Reject non-English name", False)
    except ValidationFailedError:
        print_result("Reject non-English name", True)
    except Exception as e:
        print_result("Reject non-English name", False)
        print(e)


if __name__ == "__main__":
    print("\nRunning Publisher tests...\n")
    test_delete_all()
    test_create_publisher()
    test_invalid_name()
