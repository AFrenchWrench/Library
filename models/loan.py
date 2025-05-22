from __future__ import annotations
from datetime import date
from mysql.connector import Error
from db import get_connection
from models.db_exceptions import ValidationFailedError, DatabaseOperationError
from models.validators import LoanValidator


class Loan:
    def __init__(
        self,
        member_id: int,
        book_id: int,
        loan_date: date,
        due_date: date,
        return_date: date | None = None,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.member_id = member_id
        self.book_id = book_id
        self.loan_date = loan_date
        self.due_date = due_date
        self.return_date = return_date

    def validate(self) -> None:
        validator = LoanValidator()
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
            raise DatabaseOperationError(f"Database error: {err}") from err

    def _build_query(self) -> tuple[str, tuple]:
        if self.id is None:
            return (
                "INSERT INTO loans (member_id, book_id, loan_date, due_date, return_date) VALUES (%s, %s, %s, %s, %s)",
                (
                    self.member_id,
                    self.book_id,
                    self.loan_date,
                    self.due_date,
                    self.return_date,
                ),
            )
        else:
            return (
                "UPDATE loans SET return_date=%s WHERE id=%s",
                (self.return_date, self.id),
            )

    @classmethod
    def delete_all(cls) -> None:
        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute("DELETE FROM loans;")
                    conn.commit()
        except Exception as e:
            raise DatabaseOperationError("Failed to delete loans.") from e
