from __future__ import annotations
from typing import Literal
from db import get_connection
from datetime import date
from mysql.connector import Error
from models.db_exceptions import AdminAlreadyExistsError, UserNotFound


class Member:
    def __init__(
        self,
        id=None,
        name=None,
        email=None,
        password_hash=None,
        joined_date=None,
        role="member",
    ) -> None:
        self.id: None | int = id
        self.name: str = name
        self.email: str = email
        self.password_hash: str = password_hash
        self.joined_date: str = joined_date if joined_date else date.today()
        if role not in ("admin", "member"):
            raise ValueError(f"Invalid role: {role}")
        self.role: Literal["member"] | Literal["admin"] = role

    def save(self) -> None:
        conn = get_connection()
        cur = conn.cursor()
        try:
            if self.id is None:
                cur.execute(
                    "INSERT INTO members (name, email, password_hash, joined_date, role) VALUES (%s,%s,%s,%s,%s)",
                    (
                        self.name,
                        self.email,
                        self.password_hash,
                        self.joined_date,
                        self.role,
                    ),
                )
                self.id = cur.lastrowid
            else:
                cur.execute(
                    "UPDATE members SET name=%s, email=%s, password_hash=%s WHERE id=%s",
                    (self.name, self.email, self.password_hash, self.id),
                )
            conn.commit()
        except Error as err:
            conn.rollback()
            if err.errno == 1644:
                raise AdminAlreadyExistsError("Only one admin is allowed.") from err
            else:
                raise
        finally:
            cur.close()
            conn.close()

    @staticmethod
    def get_by_email(email) -> Member:
        conn = get_connection()
        cur = conn.cursor(dictionary=True)
        cur.execute("SELECT * FROM members WHERE email=%s", (email,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        if not row:
            raise UserNotFound(f"No User found with the email:{email}")
        return Member(**row)

    @staticmethod
    def delete_all_members() -> None:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM members;")
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()
