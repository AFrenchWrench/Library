from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import PublisherValidator
from models.exceptions import (
    DatabaseOperationError,
    DuplicateNameError,
    PublisherNotFound,
    ValidationFailedError,
    PublisherInUse,
)


class Publisher:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.id: int | None = id
        self.name: str = name

    def validate(self) -> None:
        validator = PublisherValidator()
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
                    f"Publisher with name '{self.name}' already exists."
                )
            raise DatabaseOperationError(f"Unexpected database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO publishers (name) VALUES (%s)",
                (self.name,),
            )
        else:
            return (
                "UPDATE publishers SET name=%s WHERE id=%s",
                (self.name, self.id),
            )

    @classmethod
    def get_by_id(cls, publisher_id: int) -> Publisher:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM publishers WHERE id = %s", (publisher_id,))
                row = cur.fetchone()
                if not row:
                    raise PublisherNotFound(
                        f"No publisher found with ID {publisher_id}"
                    )
                return cls(**row)

    @classmethod
    def get_by_name(cls, name: str) -> Publisher:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM publishers WHERE name=%s", (name,))
                row = cur.fetchone()
        if not row:
            raise PublisherNotFound(f"No publisher found with name '{name}'")
        return cls(**row)

    @classmethod
    def delete_by_name(cls, name: str) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor(dictionary=True) as cur:
                    cur.execute("SELECT id FROM publishers WHERE name = %s", (name,))
                    result = cur.fetchone()
                    if not result:
                        raise PublisherNotFound(
                            f"No publisher found with name '{name}'"
                        )

                    publisher_id = result["id"]

                    try:
                        cur.execute(
                            "DELETE FROM publishers WHERE id = %s", (publisher_id,)
                        )
                        conn.commit()
                    except Error as err:
                        if err.errno == 1451:
                            cur.execute(
                                "SELECT title FROM books WHERE publisher_id = %s",
                                (publisher_id,),
                            )
                            books = cur.fetchall()
                            titles = [row["title"] for row in books]
                            title_list = ", ".join(f"'{t}'" for t in titles)
                            raise PublisherInUse(
                                f"Cannot delete publisher '{name}' because it is referenced by the following books: {title_list}"
                            ) from err
                        raise

        except Error as err:
            raise DatabaseOperationError("Failed to delete publisher.") from err
