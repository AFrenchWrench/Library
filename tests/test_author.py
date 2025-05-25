from models.author import Author
from models.book import Book
from models.category import Category
from models.publisher import Publisher
from models.exceptions import (
    AuthorInUse,
    ValidationFailedError,
    DuplicateNameError,
    AuthorNotFound,
    PublisherInUse,
    CategoryInUse,
)


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def test_create_valid_author():
    try:
        author = Author(name="J.K. Rowling")
        author.save()
        print_result("Create valid author", True)
    except Exception as e:
        print_result("Create valid author", False)
        print(e)
    finally:
        Author.delete_by_name("J.K. Rowling")


def test_duplicate_author():
    try:
        a1 = Author(name="George Orwell")
        a1.save()

        a2 = Author(name="George Orwell")
        a2.save()

        print_result("Reject duplicate author", False)
    except DuplicateNameError:
        print_result("Reject duplicate author", True)
    except Exception as e:
        print_result("Reject duplicate author", False)
        print(e)
    finally:
        Author.delete_by_name("George Orwell")


def test_empty_author_name():
    try:
        author = Author(name="")
        author.save()
        print_result("Reject empty author name", False)
    except ValidationFailedError:
        print_result("Reject empty author name", True)
    except Exception as e:
        print_result("Reject empty author name", False)
        print(e)


def test_non_english_author_name():
    try:
        author = Author(name="نویسنده تستی")
        author.save()
        print_result("Reject non-English author name", False)
    except ValidationFailedError:
        print_result("Reject non-English author name", True)
    except Exception as e:
        print_result("Reject non-English author name", False)
        print(e)


def test_get_author_by_name():
    try:
        author = Author(name="Isaac Asimov")
        author.save()
        fetched = Author.get_by_name("Isaac Asimov")
        if fetched.name == "Isaac Asimov":
            print_result("Get author by name", True)
        else:
            print_result("Get author by name", False)
    except Exception as e:
        print_result("Get author by name", False)
        print(e)
    finally:
        Author.delete_by_name("Isaac Asimov")


def test_get_nonexistent_author():
    try:
        Author.get_by_name("NoSuchAuthor")
        print_result("Handle non-existent author", False)
    except AuthorNotFound:
        print_result("Handle non-existent author", True)
    except Exception as e:
        print_result("Handle non-existent author", False)
        print(e)


def test_update_author():
    try:
        author = Author(name="UpdateTest Author")
        author.save()
        author.name = "Updated Author"
        author.save()
        updated = Author.get_by_name("Updated Author")
        if updated.name == "Updated Author":
            print_result("Update author name", True)
        else:
            print_result("Update author name", False)
    except Exception as e:
        print_result("Update author name", False)
        print(e)
    finally:
        try:
            Author.delete_by_name("UpdateTest Author")
        except:
            pass
        try:
            Author.delete_by_name("Updated Author")
        except:
            pass


def test_delete_author():
    try:
        author = Author(name="TempAuthor")
        author.save()
        Author.delete_by_name("TempAuthor")
        try:
            Author.get_by_name("TempAuthor")
            print_result("Delete author by name", False)
        except AuthorNotFound:
            print_result("Delete author by name", True)
    except Exception as e:
        print_result("Delete author by name", False)
        print(e)


def test_delete_nonexistent_author():
    try:
        Author.delete_by_name("GhostAuthor")
        print_result("Delete non-existent author", False)
    except AuthorNotFound:
        print_result("Delete non-existent author", True)
    except Exception as e:
        print_result("Delete non-existent author", False)
        print(e)


def test_author_in_use():
    try:
        author = Author(name="InUse Author")
        author.save()

        publisher = Publisher(name="Temp Publisher")
        publisher.save()

        category = Category(name="Temp Category")
        category.save()

        book = Book(
            isbn="9988776655",
            title="Book By Author",
            author_id=author.id,
            publisher_id=publisher.id,
            category_id=category.id,
            total_copies=5,
            available_copies=5,
        )
        book.save()

        try:
            Author.delete_by_name("InUse Author")
            print_result("Reject deletion of in-use author", False)
        except AuthorInUse:
            print_result("Reject deletion of in-use author", True)
        except Exception as e:
            print_result("Reject deletion of in-use author", False)
            print(e)

    except Exception as e:
        print_result("Reject deletion of in-use author", False)
        print(e)
    finally:
        Book.delete_by_isbn("9988776655")
        try:
            Publisher.delete_by_name("Temp Publisher")
        except PublisherInUse:
            pass
        try:
            Category.delete_by_name("Temp Category")
        except CategoryInUse:
            pass
        try:
            Author.delete_by_name("InUse Author")
        except AuthorInUse:
            pass


if __name__ == "__main__":
    print("\nRunning Author tests...\n")
    test_create_valid_author()
    test_duplicate_author()
    test_empty_author_name()
    test_non_english_author_name()
    test_get_author_by_name()
    test_get_nonexistent_author()
    test_update_author()
    test_delete_author()
    test_delete_nonexistent_author()
    test_author_in_use()
