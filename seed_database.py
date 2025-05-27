from faker import Faker
import random
from datetime import timedelta, date

from models.author import Author
from models.book import Book
from models.category import Category
from models.loan import Loan
from models.publisher import Publisher
from models.user import User


fake = Faker()
Faker.seed(0)
random.seed(0)


def clean_name(text, min_len=5, max_len=15):
    text = "".join(filter(str.isalnum, text))
    if len(text) < min_len:
        return clean_name(fake.word(), min_len, max_len)
    return text[:max_len]


author_ids = []
publisher_ids = []
category_ids = []
book_ids = []
user_ids = []
loan_ids = []

for _ in range(100):
    author = Author(name=clean_name(fake.unique.name()))
    try:
        author.save()
        author_ids.append(author.id)
    except Exception as e:
        print(f"Failed to save author: {e}")

for _ in range(100):
    publisher = Publisher(name=clean_name(fake.unique.company()))
    try:
        publisher.save()
        publisher_ids.append(publisher.id)
    except Exception as e:
        print(f"Failed to save publisher: {e}")

for _ in range(100):
    category = Category(name=clean_name(fake.unique.word()))
    try:
        category.save()
        category_ids.append(category.id)
    except Exception as e:
        print(f"Failed to save category: {e}")

for _ in range(100):
    user = User(
        name=clean_name(fake.unique.name()),
        email=fake.unique.email(),
        password=fake.password(length=10),
        role="member",
    )
    try:
        user.save()
        user_ids.append(user.id)
    except Exception as e:
        print(f"Failed to save user: {e}")

for _ in range(100):
    book = Book(
        isbn=fake.unique.isbn13(),
        title=fake.unique.sentence(nb_words=4).rstrip("."),
        author_id=random.choice(author_ids),
        publisher_id=random.choice(publisher_ids),
        category_id=random.choice(category_ids),
        total_copies=random.randint(100, 150),
        available_copies=random.randint(80, 100),
    )
    try:
        book.save()
        book_ids.append(book.id)
    except Exception as e:
        print(f"Failed to save book: {e}")

for _ in range(100):
    returned = random.choice([True, False])
    return_date = (
        fake.date_between(
            start_date=(date.today() + timedelta(4)),
            end_date=(date.today() + timedelta(21)),
        )
        if returned
        else None
    )

    loan = Loan(
        user_id=random.choice(user_ids),
        book_id=random.choice(book_ids),
        return_date=return_date,
    )
    try:
        loan.save()
        loan.check_for_fine()
        loan_ids.append(loan.id)
    except Exception as e:
        print(f"Failed to save loan: {e}")
