from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import AuthorValidator
from models.exceptions import (
    AuthorInUse,
    DatabaseOperationError,
    DuplicateNameError,
    AuthorNotFound,
    ValidationFailedError,
)


class Author:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.id: int | None = id
        self.name: str = name

    def validate(self) -> None:
        validator = AuthorValidator()
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
            if err.errno == 1062 and "name" in err.msg.lower():
                raise DuplicateNameError(
                    f"Author with name '{self.name}' already exists."
                )
            raise DatabaseOperationError(f"Unexpected database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO authors (name) VALUES (%s)",
                (self.name,),
            )
        else:
            return (
                "UPDATE authors SET name=%s WHERE id=%s",
                (self.name, self.id),
            )

    @classmethod
    def get_by_id(cls, author_id: int) -> Author:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM authors WHERE id = %s", (author_id,))
                row = cur.fetchone()
                if not row:
                    raise AuthorNotFound(f"No author found with ID {author_id}")
                return cls(**row)

    @classmethod
    def get_by_name(cls, name: str) -> Author:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM authors WHERE name=%s", (name,))
                row = cur.fetchone()
        if not row:
            raise AuthorNotFound(f"No author found with name '{name}'")
        return cls(**row)

    @classmethod
    def delete_by_name(cls, name: str) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT id FROM authors WHERE name = %s", (name,))
                    result = cur.fetchone()
                    if not result:
                        raise AuthorNotFound(f"No author found with name '{name}'")

                    author_id = result["id"]

                    try:
                        cur.execute("DELETE FROM authors WHERE id = %s", (author_id,))
                        conn.commit()
                    except Error as err:
                        if err.errno == 1451:
                            cur.execute(
                                "SELECT title FROM books WHERE author_id = %s",
                                (author_id,),
                            )
                            books = cur.fetchall()
                            titles = [row["title"] for row in books]
                            title_list = ", ".join(f"'{t}'" for t in titles)
                            raise AuthorInUse(
                                f"Cannot delete author '{name}' because it is referenced by the following books: {title_list}"
                            ) from err
                        raise

        except Error as err:
            raise DatabaseOperationError("Failed to delete author.") from err
