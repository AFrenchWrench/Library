from datetime import date
from re import match
from db import get_connection


class GeneralValidator:

    @staticmethod
    def validate_to_be_in_english(text: str) -> bool:
        if not isinstance(text, str) or not text.isascii():
            raise ValueError(f"Text '{text}' must be fully in English.")
        return True

    @staticmethod
    def validate_to_be_whole_number(number):
        if not isinstance(number, (int, float)):
            raise ValueError("Input must be a number.")
        if number % 1 != 0:
            raise ValueError("Number must be whole (no decimals).")
        if number < 0:
            raise ValueError("Number must be a non negative int")
        return True

    @staticmethod
    def validate_date(d: date):
        today = date.today()
        if not isinstance(d, date):
            raise ValueError("The input is not a valid date.")
        elif d < today:
            raise ValueError("Date cannot be in the past.")
        elif (d - today).days > 60:
            raise ValueError("Date can't be more than 60 days ahead.")
        return True


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
        return True


class AuthorValidator(GeneralValidator):
    def validate_name(self, name):
        self.validate_to_be_in_english(name)

        if len(name) < 3:
            raise ValueError("Name is too short")
        elif len(name) > 20:
            raise ValueError("Name is too long")
        return True

    def validate(self, book):
        errors = {}

        attrs = ["name"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(book, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))
        return True


class PublisherValidator(GeneralValidator):

    def validate_name(self, name):
        self.validate_to_be_in_english(name)

        if len(name) < 3:
            raise ValueError("Name is too short")
        elif len(name) > 20:
            raise ValueError("Name is too long")
        return True

    def validate(self, book):
        errors = {}

        attrs = ["name"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(book, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))
        return True


class CategoryValidator(GeneralValidator):

    def validate_name(self, name):
        self.validate_to_be_in_english(name)

        if len(name) < 3:
            raise ValueError("Name is too short")
        elif len(name) > 20:
            raise ValueError("Name is too long")
        return True

    def validate(self, book):
        errors = {}

        attrs = ["name"]

        for attr in attrs:
            validator_name = f"validate_{attr}"
            validator = getattr(self, validator_name, None)
            if callable(validator):
                value = getattr(book, attr)
                try:
                    if value is None or value == "":
                        raise ValueError("Field can't be empty.")
                    validator(value)
                except ValueError as e:
                    errors[attr] = str(e)

        if errors:
            raise ValueError("\n".join(f"{k}: {v}" for k, v in errors.items()))
        return True
