from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.validators import CategoryValidator
from models.exceptions import (
    DatabaseOperationError,
    DuplicateNameError,
    CategoryNotFound,
    ValidationFailedError,
)


class Category:
    def __init__(self, name: str, id: int | None = None) -> None:
        self.id = id
        self.name = name

    def validate(self) -> None:
        validator = CategoryValidator()
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
                    f"Category with name '{self.name}' already exists."
                )
            raise DatabaseOperationError(f"Unexpected database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO categories (name) VALUES (%s)",
                (self.name,),
            )
        else:
            return (
                "UPDATE categories SET name=%s WHERE id=%s",
                (self.name, self.id),
            )

    @classmethod
    def get_by_id(cls, id: int) -> Category:
        with get_connection() as conn:
            with conn.cursor(dictionary=True) as cur:
                cur.execute("SELECT * FROM categories WHERE id=%s", (id,))
                row = cur.fetchone()
        if not row:
            raise CategoryNotFound(f"No category found with ID {id}")
        return cls(**row)

    @classmethod
    def delete_all(cls) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM categories;")
                    conn.commit()
        except Exception as e:
            raise DatabaseOperationError("Failed to delete categories.") from e
