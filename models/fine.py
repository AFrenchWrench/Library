from __future__ import annotations
from mysql.connector import Error
from db import get_connection
from models.exceptions import ValidationFailedError, DatabaseOperationError
from models.validators import FineValidator


class Fine:
    def __init__(
        self,
        user_id: int,
        loan_id: int,
        amount: float,
        paid: bool = False,
        id: int | None = None,
    ) -> None:
        self.id = id
        self.user_id = user_id
        self.loan_id = loan_id
        self.amount = amount
        self.paid = paid

    def validate(self) -> None:
        validator = FineValidator()
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
                "INSERT INTO fines (user_id, loan_id, amount, paid) VALUES (%s, %s, %s, %s)",
                (self.user_id, self.loan_id, self.amount, self.paid),
            )
        else:
            return (
                "UPDATE fines SET amount=%s, paid=%s WHERE id=%s",
                (self.amount, self.paid, self.id),
            )
