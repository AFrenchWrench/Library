from models.author import Author
from models.book import Book
from models.category import Category
from models.publisher import Publisher
from models.exceptions import (
    AuthorInUse,
    CategoryInUse,
    DuplicateNameError,
    PublisherInUse,
    ValidationFailedError,
    PublisherNotFound,
)


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_create_valid_publisher():
    try:
        publisher = Publisher(name="Valid Publisher")
        publisher.save()
        print_result("Create valid publisher", True)
    except Exception as e:
        print_result("Create valid publisher", False)
        print(e)
    finally:
        Publisher.delete_by_name(publisher.name)


def test_duplicate_publisher():
    try:
        publisher = Publisher(name="Duplicate Publisher")
        publisher.save()

        duplicate = Publisher(name="Duplicate Publisher")
        duplicate.save()

        print_result("Reject duplicate publisher", False)
    except DuplicateNameError:
        print_result("Reject duplicate publisher", True)
    except Exception as e:
        print_result("Reject duplicate publisher", False)
        print(e)
    finally:
        Publisher.delete_by_name(publisher.name)


def test_empty_name():
    try:
        publisher = Publisher(name="")
        publisher.save()
        print_result("Reject empty name", False)
    except ValidationFailedError:
        print_result("Reject empty name", True)
    except Exception as e:
        print_result("Reject empty name", False)
        print(e)


def test_non_english_name():
    try:
        publisher = Publisher(name="انتشارات")
        publisher.save()
        print_result("Reject non-English name", False)
    except ValidationFailedError:
        print_result("Reject non-English name", True)
    except Exception as e:
        print_result("Reject non-English name", False)
        print(e)


def test_long_name():
    try:
        publisher = Publisher(name="P" * 101)
        publisher.save()
        print_result("Reject long name", False)
    except ValidationFailedError:
        print_result("Reject long name", True)
    except Exception as e:
        print_result("Reject long name", False)
        print(e)


def test_get_by_name():
    try:
        publisher = Publisher(name="Get Test Publisher")
        publisher.save()
        fetched = Publisher.get_by_name(publisher.name)
        if fetched.name == "Get Test Publisher":
            print_result("Get publisher by Name", True)
        else:
            print_result("Get publisher by Name", False)
    except Exception as e:
        print_result("Get publisher by Name", False)
        print(e)
    finally:
        Publisher.delete_by_name(publisher.name)


def test_get_nonexistent_publisher():
    try:
        Publisher.get_by_name("Non-existent")
        print_result("Handle non-existent publisher", False)
    except PublisherNotFound:
        print_result("Handle non-existent publisher", True)
    except Exception as e:
        print_result("Handle non-existent publisher", False)
        print(e)


def test_update_publisher_name():
    try:
        publisher = Publisher(name="Original Name")
        publisher.save()

        publisher.name = "Updated Name"
        publisher.save()

        updated = Publisher.get_by_name(publisher.name)
        if updated.name == "Updated Name":
            print_result("Update publisher name", True)
        else:
            print_result("Update publisher name", False)
    except Exception as e:
        print_result("Update publisher name", False)
        print(e)
    finally:
        try:
            Publisher.delete_by_name("Original Name")
        except:
            pass
        try:
            Publisher.delete_by_name("Updated Name")
        except:
            pass


def test_delete_by_name():
    try:
        publisher = Publisher(name="Delete Test")
        publisher.save()

        Publisher.delete_by_name(publisher.name)

        try:
            Publisher.get_by_name(publisher.name)
            print_result("Delete publisher by Name", False)
        except PublisherNotFound:
            print_result("Delete publisher by Name", True)

    except Exception as e:
        print_result("Delete publisher by Name", False)
        print(e)


def test_publisher_in_use():
    try:
        author = Author(name="Temp Author")
        author.save()

        publisher = Publisher(name="InUse Publisher")
        publisher.save()

        category = Category(name="Temp Category")
        category.save()

        book = Book(
            isbn="1122334455",
            title="Book Using Category",
            author_id=author.id,
            publisher_id=publisher.id,
            category_id=category.id,
            total_copies=3,
            available_copies=3,
        )
        book.save()

        try:
            Publisher.delete_by_name("InUse Publisher")
            print_result("Reject deletion of in-use publisher", False)
        except PublisherInUse:
            print_result("Reject deletion of in-use publisher", True)
        except Exception as e:
            print_result("Reject deletion of in-use publisher", False)
            print(e)

    except Exception as e:
        print_result("Reject deletion of in-use publisher", False)
        print(e)
    finally:
        Book.delete_by_isbn("1122334455")
        try:
            Author.delete_by_name("Temp Author")
        except AuthorInUse:
            pass
        try:
            Publisher.delete_by_name("InUse Publisher")
        except PublisherInUse:
            pass
        try:
            Category.delete_by_name("Temp Category")
        except CategoryInUse:
            pass


if __name__ == "__main__":
    print("\nRunning Publisher tests...\n")
    test_create_valid_publisher()
    test_duplicate_publisher()
    test_empty_name()
    test_non_english_name()
    test_long_name()
    test_get_by_name()
    test_get_nonexistent_publisher()
    test_update_publisher_name()
    test_delete_by_name()
    test_publisher_in_use()
