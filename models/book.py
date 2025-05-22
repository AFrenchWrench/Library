from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import BookValidator
from models.db_exceptions import (
    DatabaseOperationError,
    DuplicateISBNError,
    ValidationFailedError,
    BookNotFound,
)


class Book:
    def __init__(
        self,
        isbn: str,
        title: str,
        author_id: int,
        publisher_id: int,
        category_id: int,
        total_copies: int = 1,
        available_copies: int = 1,
        id: int | None = None,
    ) -> None:
        self.id: int | None = id
        self.isbn: str = isbn
        self.title: str = title
        self.author_id: int = author_id
        self.publisher_id: int = publisher_id
        self.category_id: int = category_id
        self.total_copies: int = total_copies
        self.available_copies: int = available_copies

    def validate(self) -> None:
        validator = BookValidator()
        validator.validate(self)

    def save(self) -> bool:
        try:
            self.validate()
        except ValueError as e:
            raise ValidationFailedError(f"Validation failed:\n{e}") from e

        query, values = self._build_query()

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, values)
                    if self.id is None:
                        self.id = cur.lastrowid
                    conn.commit()
            return True
        except Error as err:
            if err.errno == 1062 and "isbn" in err.msg.lower():
                raise DuplicateISBNError(
                    f"Book with this ISBN already exists: {self.isbn}"
                ) from err
            else:
                raise DatabaseOperationError(
                    f"Unexpected database error: {err}"
                ) from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                """
                INSERT INTO books (isbn, title, author_id, publisher_id, category_id, total_copies, available_copies)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    self.isbn,
                    self.title,
                    self.author_id,
                    self.publisher_id,
                    self.category_id,
                    self.total_copies,
                    self.available_copies,
                ),
            )
        else:
            return (
                """
                UPDATE books
                SET isbn=%s, title=%s, author_id=%s, publisher_id=%s, category_id=%s,
                    total_copies=%s, available_copies=%s
                WHERE id=%s
                """,
                (
                    self.isbn,
                    self.title,
                    self.author_id,
                    self.publisher_id,
                    self.category_id,
                    self.total_copies,
                    self.available_copies,
                    self.id,
                ),
            )

    @classmethod
    def get_by_isbn(cls, isbn: str) -> Book:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM books WHERE isbn=%s", (isbn,))
                row = cur.fetchone()
        if not row:
            raise BookNotFound(f"No book found with ISBN: {isbn}")
        return cls(**row)

    @classmethod
    def delete_by_isbn(cls, isbn: str) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM books WHERE isbn = %s", (isbn,))
                    if cur.rowcount == 0:
                        raise BookNotFound(f"No book found with ISBN: {isbn}")
                    conn.commit()
        except BookNotFound:
            raise
        except Exception as e:
            raise DatabaseOperationError(
                f"Failed to delete book with ISBN: {isbn}"
            ) from e

    @classmethod
    def delete_all(cls) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM books")
                    conn.commit()
        except Exception as e:
            raise DatabaseOperationError("Failed to delete books.") from e
