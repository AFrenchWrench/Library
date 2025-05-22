from models.publisher import Publisher
from models.exceptions import ValidationFailedError, PublisherNotFound
from db import get_connection

seeded_publisher_id = None


def print_result(test_name, passed):
    print(f"{'✅' if passed else '❌'} {test_name}")


def seed_required_publisher():
    global seeded_publisher_id
    publisher = Publisher(name="Seeded Publisher")
    publisher.save()
    seeded_publisher_id = publisher.id


def delete_seeded_publisher():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"DELETE FROM publishers WHERE id = {seeded_publisher_id} AND name = 'Seeded Publisher'"
            )
            conn.commit()


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
        Publisher.delete_by_name(publisher.name)


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


if __name__ == "__main__":
    print("\nRunning Publisher tests...\n")
    seed_required_publisher()

    try:
        test_create_valid_publisher()
        test_empty_name()
        test_non_english_name()
        test_long_name()
        test_get_by_name()
        test_get_nonexistent_publisher()
        test_update_publisher_name()
        test_delete_by_name()
    finally:
        print("\nCleaning up seeded publisher...")
        delete_seeded_publisher()
        print("Cleanup complete.")
