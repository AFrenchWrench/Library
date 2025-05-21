from datetime import date
from re import match
from db import get_connection


class GeneralValidator:

    @staticmethod
    def validate_to_be_in_english(text: str) -> bool:
        if not isinstance(text, str) or not text.isascii():
            raise ValueError(f"Text '{text}' must be fully in English.")

    @staticmethod
    def validate_to_be_whole_number(number):
        if not isinstance(number, (int, float)):
            raise ValueError("Input must be a number.")
        if number % 1 != 0:
            raise ValueError("Number must be whole (no decimals).")
        if number < 0:
            raise ValueError("Number must be a non negative int")

    @staticmethod
    def validate_date(d: date):
        today = date.today()
        if not isinstance(d, date):
            raise ValueError("The input is not a valid date.")
        elif d < today:
            raise ValueError("Date cannot be in the past.")
        elif (d - today).days > 60:
            raise ValueError("Date can't be more than 60 days ahead.")

    @staticmethod
    def validate_foreign_key_exists(table: str, id_value: int):
        GeneralValidator.validate_to_be_whole_number(id_value)

        query = f"SELECT 1 FROM {table} WHERE id = %s LIMIT 1"
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (id_value,))
                    result = cur.fetchone()
                    if not result:
                        raise ValueError(
                            f"No entry found in '{table}' with id={id_value}"
                        )
        except Exception as e:
            raise ValueError(f"Error validating foreign key for '{table}': {e}")


class MemberValidator(GeneralValidator):

    def validate_name(self, name):
        self.validate_to_be_in_english(name)
        if len(name) < 3:
            raise ValueError("name is too short")

    def validate_email(self, email):
        self.validate_to_be_in_english(email)
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not match(pattern, email):
            raise ValueError("Email is not in valid form")

    def validate_password(self, password):
        self.validate_to_be_in_english(password)
        pattern = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^A-Za-z\d]).{8,}$"
        if not match(pattern, password):
            raise ValueError(
                "Password must be at least 8 characters long, with one uppercase, one number, and one special character."
            )

    def validate_joined_date(self, joined_date):
        self.validate_date(joined_date)

    def validate_role(self, role):
        self.validate_to_be_in_english(role)
        if role not in ("admin", "member"):
            raise ValueError(
                f"Role '{role}' is not valid. Must be 'admin' or 'member'."
            )

    def validate(self, member):
        errors = {}

        attrs = ["name", "email", "password", "joined_date", "role"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(member, attr)
                try:
                    if value == "" or value == None:
                        raise ValueError("Field can't be empty")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))


class AuthorValidator(GeneralValidator):

    def validate_name(self, name):
        self.validate_to_be_in_english(name)

        if len(name) < 3:
            raise ValueError("Name is too short")
        elif len(name) > 20:
            raise ValueError("Name is too long")

    def validate(self, author):
        errors = {}

        attrs = ["name"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(author, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))


class PublisherValidator(GeneralValidator):

    def validate_name(self, name):
        self.validate_to_be_in_english(name)

        if len(name) < 3:
            raise ValueError("Name is too short")
        elif len(name) > 20:
            raise ValueError("Name is too long")

    def validate(self, publisher):
        errors = {}

        attrs = ["name"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(publisher, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))


class CategoryValidator(GeneralValidator):

    def validate_name(self, name):
        self.validate_to_be_in_english(name)

        if len(name) < 3:
            raise ValueError("Name is too short")
        elif len(name) > 20:
            raise ValueError("Name is too long")

    def validate(self, category):
        errors = {}

        attrs = ["name"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(category, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))


class BookValidator(GeneralValidator):

    def validate_isbn(self, isbn):
        self.validate_to_be_in_english(isbn)
        if len(isbn) < 8:
            raise ValueError("ISBN is too short.")
        if len(isbn) > 20:
            raise ValueError("ISBN is too long.")

    def validate_title(self, title):
        self.validate_to_be_in_english(title)
        if len(title) < 2:
            raise ValueError("Title is too short.")
        if len(title) > 255:
            raise ValueError("Title is too long.")

    def validate_author_id(self, author_id):
        self.validate_foreign_key_exists("authors", author_id)

    def validate_publisher_id(self, publisher_id):
        self.validate_foreign_key_exists("publishers", publisher_id)

    def validate_category_id(self, category_id):
        self.validate_foreign_key_exists("categories", category_id)

    def validate_total_copies(self, total_copies):
        self.validate_to_be_whole_number(total_copies)

    def validate_available_copies(self, available_copies, total_copies):
        self.validate_to_be_whole_number(available_copies)

        if available_copies > total_copies:
            raise ValueError("Available copies cannot be more than total copies.")

    def validate(self, book):
        errors = {}

        attrs = [
            "isbn",
            "title",
            "author_id",
            "publisher_id",
            "category_id",
            "total_copies",
            "available_copies",
        ]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(book, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    (
                        validator(value)
                        if attr != "available_copies"
                        else validator(value, getattr(book, "total_copies"))
                    )
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))
