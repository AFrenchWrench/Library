from models.author import Author
from models.book import Book
from models.category import Category
from models.publisher import Publisher
from models.exceptions import (
    AuthorInUse,
    PublisherInUse,
    ValidationFailedError,
    DuplicateNameError,
    CategoryNotFound,
    CategoryInUse,
)


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_create_valid_category():
    try:
        cat = Category(name="Programming")
        cat.save()
        print_result("Create valid category", True)
    except Exception as e:
        print_result("Create valid category", False)
        print(e)
    finally:
        Category.delete_by_name("Programming")


def test_duplicate_category():
    try:
        cat1 = Category(name="Fiction")
        cat1.save()

        cat2 = Category(name="Fiction")
        cat2.save()

        print_result("Reject duplicate category", False)
    except DuplicateNameError:
        print_result("Reject duplicate category", True)
    except Exception as e:
        print_result("Reject duplicate category", False)
        print(e)
    finally:
        Category.delete_by_name(name="Fiction")


def test_empty_category_name():
    try:
        cat = Category(name="")
        cat.save()
        print_result("Reject empty category name", False)
    except ValidationFailedError:
        print_result("Reject empty category name", True)
    except Exception as e:
        print_result("Reject empty category name", False)
        print(e)


def test_non_english_category():
    try:
        cat = Category(name="دسته بندی")
        cat.save()
        print_result("Reject non-English category name", False)
    except ValidationFailedError:
        print_result("Reject non-English category name", True)
    except Exception as e:
        print_result("Reject non-English category name", False)
        print(e)


def test_get_by_name():
    try:
        cat = Category(name="History")
        cat.save()
        found = Category.get_by_name("History")
        if found.name == "History":
            print_result("Get category by name", True)
        else:
            print_result("Get category by name", False)
    except Exception as e:
        print_result("Get category by name", False)
        print(e)
    finally:
        Category.delete_by_name("History")


def test_get_nonexistent_category():
    try:
        Category.get_by_name("NoSuchCategory")
        print_result("Handle non-existent category", False)
    except CategoryNotFound:
        print_result("Handle non-existent category", True)
    except Exception as e:
        print_result("Handle non-existent category", False)
        print(e)


def test_update_category():
    try:
        cat = Category(name="UpdateTest")
        cat.save()
        cat.name = "UpdatedCategory"
        cat.save()
        updated = Category.get_by_name("UpdatedCategory")
        if updated.name == "UpdatedCategory":
            print_result("Update category name", True)
        else:
            print_result("Update category name", False)
    except Exception as e:
        print_result("Update category name", False)
        print(e)
    finally:
        try:
            Category.delete_by_name("UpdateTest")
        except:
            pass
        try:
            Category.delete_by_name("UpdatedCategory")
        except:
            pass


def test_delete_category():
    try:
        cat = Category(name="TempToDelete")
        cat.save()
        Category.delete_by_name("TempToDelete")
        try:
            Category.get_by_name("TempToDelete")
            print_result("Delete category by name", False)
        except CategoryNotFound:
            print_result("Delete category by name", True)
    except Exception as e:
        print_result("Delete category by name", False)
        print(e)


def test_delete_nonexistent_category():
    try:
        Category.delete_by_name("GhostCategory")
        print_result("Delete non-existent category", False)
    except CategoryNotFound:
        print_result("Delete non-existent category", True)
    except Exception as e:
        print_result("Delete non-existent category", False)
        print(e)


def test_category_in_use():
    try:
        author = Author(name="Temp Author")
        author.save()

        publisher = Publisher(name="Temp Publisher")
        publisher.save()

        category = Category(name="InUse Category")
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
            Category.delete_by_name("InUse Category")
            print_result("Reject deletion of in-use category", False)
        except CategoryInUse:
            print_result("Reject deletion of in-use category", True)
        except Exception as e:
            print_result("Reject deletion of in-use category", False)
            print(e)

    except Exception as e:
        print_result("Reject deletion of in-use category", False)
        print(e)
    finally:
        Book.delete_by_isbn("1122334455")
        try:
            Author.delete_by_name("Temp Author")
        except AuthorInUse:
            pass
        try:
            Publisher.delete_by_name("Temp Publisher")
        except PublisherInUse:
            pass
        try:
            Category.delete_by_name("InUse Category")
        except CategoryInUse:
            pass


if __name__ == "__main__":
    print("\nRunning Category tests...\n")
    test_create_valid_category()
    test_duplicate_category()
    test_empty_category_name()
    test_non_english_category()
    test_get_by_name()
    test_get_nonexistent_category()
    test_update_category()
    test_delete_category()
    test_delete_nonexistent_category()
    test_category_in_use()
